
# Personal Portfolio Website

A responsive personal portfolio website for a second-year Computer Science and Engineering student specializing in Artificial Intelligence and Machine Learning.

## Project Structure

- `frontend/` — HTML, CSS and JavaScript portfolio.
- `backend/` — Python Flask API and SQLite message storage.

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: SQLite
- Version Control: Git and GitHub

## Run the Frontend

Open `frontend/index.html` using VS Code Live Server.

## Run the Python Backend

From the project root:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

API health check:

`http://127.0.0.1:5000/api/health`

The contact form stores messages in the SQLite database.

## Features

- Responsive portfolio website.
- About, skills, projects and certifications sections.
- Python Flask backend.
- Contact form API.
- SQLite message storage.


