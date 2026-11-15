from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
import re

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

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

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "message": "Portfolio backend is running."})

@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required."}), 400
    if len(name) > 100 or len(email) > 254 or len(message) > 3000:
        return jsonify({"error": "One or more fields are too long."}), 400
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

    return jsonify({"message": "Message received successfully."}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
