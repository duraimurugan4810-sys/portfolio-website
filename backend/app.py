
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
import re
import os
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)

CORS(app, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500"
])

DATABASE = Path(__file__).with_name("messages.db")


def init_db():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def send_email(name, visitor_email, message):
    gmail_user = os.getenv("MAIL_USERNAME")
    app_password = os.getenv("MAIL_APP_PASSWORD")
    receiver = os.getenv("MAIL_TO")

    if not gmail_user or not app_password or not receiver:
        raise RuntimeError("Gmail settings are not configured.")

    email = EmailMessage()
    email["Subject"] = f"New Portfolio Message from {name}"
    email["From"] = gmail_user
    email["To"] = receiver
    email["Reply-To"] = visitor_email

    email.set_content(f"""
You received a new message through your portfolio.

Name: {name}
Email: {visitor_email}

Message:
{message}
""")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=context
    ) as smtp:
        smtp.login(gmail_user, app_password)
        smtp.send_message(email)


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "Portfolio backend is running."
    })


@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    visitor_email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not visitor_email or not message:
        return jsonify({"error": "All fields are required."}), 400

    if len(name) > 100 or len(visitor_email) > 254 or len(message) > 3000:
        return jsonify({"error": "One or more fields are too long."}), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", visitor_email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    # Save message in SQLite
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """INSERT INTO messages (name, email, message)
               VALUES (?, ?, ?)""",
            (name, visitor_email, message)
        )

    # Send email through Gmail
    try:
        send_email(name, visitor_email, message)

    except Exception:
        app.logger.exception("Email delivery failed.")
        return jsonify({
            "error": "Message saved, but email delivery failed."
        }), 502

    return jsonify({
        "message": "Message sent successfully!"
    }), 201


init_db()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
