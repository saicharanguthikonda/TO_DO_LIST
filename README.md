# TaskFlow — Python + Streamlit To-Do App

A complete To-Do List application built using only Python and Streamlit.

## Features

- Add, edit, delete, complete and reopen tasks
- Task description
- Priority: Low, Medium, High, Urgent
- Status: Pending, In Progress, Completed
- Due dates and overdue detection
- Search and filters
- Dashboard statistics
- CSV export
- Clear completed tasks
- Bright, Dark, Cool, Warm, Forest and Purple themes
- No HTML/CSS/JavaScript files
- No database dependency
- Session-state task management

## Local Deployment

### 1. Install Python
Use Python 3.12 or newer.

### 2. Open terminal in this folder

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

### 3. Install Streamlit

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
streamlit run app.py
```

Open the Local URL shown in the terminal, normally:

`http://localhost:8501`

## GitHub + Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Commit and push the files.
4. Open Streamlit Community Cloud.
5. Choose **Create app**.
6. Select your GitHub repository.
7. Select the `main` branch.
8. Set Main file path to `app.py`.
9. Select Python 3.12 in Advanced settings if available.
10. Click Deploy.

## Important

This version intentionally stores tasks in Streamlit session state. That means it is ideal for a Python/Streamlit college project and demonstration. Tasks are not a permanent shared database.

For a multi-user production system, replace session state with a persistent database such as PostgreSQL.

## Requirements

Python + Streamlit only.
