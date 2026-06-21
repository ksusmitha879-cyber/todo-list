# todo-list
# ✅ Todo List — Full Stack Task Manager

> A task manager that went from a frontend-only tutorial project to a
> real full-stack app with a Python backend and persistent storage.

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Flask](https://img.shields.io/badge/Flask-backend-black)
![SQLite](https://img.shields.io/badge/SQLite-database-blue)

## 🔗 Live Demo

- **Frontend:** _add your deployed link here_
- **Backend API:** _add your deployed link here_

## 📌 What It Does

A task manager where you can add, complete, and delete tasks — with
everything saved to a real database instead of disappearing on
refresh. Built to upgrade a basic HTML/CSS/JS todo list into a
genuine full-stack project.

## ✨ Current Features

- ➕ **Add tasks** — saved instantly to the database
- ✔️ **Mark complete/incomplete** — persists across page reloads
- 🗑️ **Delete tasks**
- 📊 **Live task stats** — total, completed, and pending counts
- 💾 **SQLite database** — no more losing tasks on refresh
- 🔌 **REST API** — clean separation between frontend and backend

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML · CSS · JavaScript |
| Backend | Python · Flask |
| Database | SQLite |
| API | REST (GET, POST, PUT, DELETE) |

## ⚙️ How It Works

```
User adds/checks/deletes a task
            ↓
   fetch() call to Flask API
            ↓
  Flask reads/writes tasks.db (SQLite)
            ↓
   Updated task list returned as JSON
            ↓
  Frontend re-renders task list + stats
```

## 📁 Project Structure

```
todo-list/
├── backend/
│   ├── app.py              # Flask server + SQLite logic
│   ├── tasks.db             # Database (auto-created)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js            # Connects to backend API
└── README.md
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Add a new task |
| PUT | `/api/tasks/<id>` | Mark complete/incomplete |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/stats` | Get total/completed/pending counts |

### Example — Add a Task

**Request:**
```json
POST /api/tasks
{
  "title": "Finish DSA practice"
}
```

**Response:**
```json
{
  "id": 4,
  "title": "Finish DSA practice",
  "completed": 0,
  "priority": "Medium",
  "category": "General",
  "created_at": "2026-06-20 18:30:00"
}
```

## 🚀 Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

API runs at `http://127.0.0.1:10000`

### Frontend

Open `frontend/index.html` with VS Code Live Server (or any local
server) so it can make API calls correctly.

## 🗺️ Roadmap

Planned upgrades to make this stand out further:

- [ ] 🤖 AI-powered task prioritization (Groq API)
- [ ] 🧩 AI task breakdown — split big tasks into subtasks automatically
- [ ] 📈 Productivity chart — visualize daily completion trends
- [ ] ☁️ Deploy backend (Render) + frontend (Netlify/GitHub Pages)

## 👩‍💻 Built By

**Karanam Susmitha**
CS Graduate | Full Stack + AI/ML 

[LinkedIn](https://www.linkedin.com/in/karanamsusmitha) ·
[GitHub](https://github.com/ksusmitha879-cyber)
