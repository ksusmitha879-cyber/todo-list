from flask import Flask, jsonify, request
from flask_cors import CORS # pyright: ignore[reportMissingModuleSource]
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ── Database setup ─────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "tasks.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            completed   INTEGER DEFAULT 0,
            priority    TEXT    DEFAULT 'Medium',
            category    TEXT    DEFAULT 'General',
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT   DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── Home route ──────────────────────────────────
@app.route("/")
def home():
    return jsonify({"message": "Todo API is running!"})

# ── GET all tasks ───────────────────────────────
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

# ── POST add new task ───────────────────────────
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data  = request.get_json()
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, priority, category) VALUES (?, ?, ?)",
        (title, data.get("priority", "Medium"),
                data.get("category", "General"))
    )
    conn.commit()

    # Return the newly created task
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    return jsonify(dict(task)), 201

# ── PUT mark task complete/incomplete ───────────
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data      = request.get_json()
    completed = data.get("completed", 0)
    completed_at = datetime.now().isoformat() if completed else None

    conn = get_db()
    conn.execute(
        "UPDATE tasks SET completed=?, completed_at=? WHERE id=?",
        (completed, completed_at, task_id)
    )
    conn.commit()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?", (task_id,)
    ).fetchone()
    conn.close()

    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(dict(task))

# ── DELETE remove a task ────────────────────────
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted", "id": task_id})

# ── GET productivity stats ──────────────────────
@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db()
    total     = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed=1"
    ).fetchone()[0]
    pending   = total - completed
    conn.close()
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)