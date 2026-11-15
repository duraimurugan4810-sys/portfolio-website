# Personal Portfolio Website

A responsive personal portfolio for an AI & Machine Learning student.

## Project structure

- `frontend/` — HTML, CSS and JavaScript portfolio
- `backend/` — Flask API and SQLite message storage

## Run the frontend

Open `frontend/index.html` with VS Code Live Server.

## Run the Python backend

From the project root:

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The API health check is available at `http://127.0.0.1:5000/api/health`.

The contact form stores messages in `backend/messages.db`.

## Before publishing

Replace the sample name, initials, email address, GitHub and LinkedIn links in `frontend/index.html`.
Replace sample project descriptions with work you have actually completed. Do not claim skills, certificates or achievements you do not have.
