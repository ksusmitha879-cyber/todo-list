// ── API connection ──────────────────────────────
const API = window.location.hostname === "localhost" ||
            window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:10000"
  : "https://your-todo-app.onrender.com";

// ── Load all tasks on page load ─────────────────
async function loadTasks() {
    const res   = await fetch(`${API}/api/tasks`);
    const tasks = await res.json();
    renderTasks(tasks);
    loadStats();
}

// ── Render tasks to DOM ─────────────────────────
function renderTasks(tasks) {
    const list = document.getElementById("task-list");
    list.innerHTML = "";

    if (tasks.length === 0) {
        list.innerHTML = `<p style="color:#888;text-align:center">
            No tasks yet — add one above!</p>`;
        return;
    }

    tasks.forEach(task => {
        const item = document.createElement("div");
        item.className = "task-item" + (task.completed ? " done" : "");
        item.innerHTML = `
            <input type="checkbox"
                ${task.completed ? "checked" : ""}
                onchange="toggleTask(${task.id}, this.checked)"/>
            <span class="task-title
                ${task.completed ? "strikethrough" : ""}">
                ${task.title}
            </span>
            <span class="priority-badge ${task.priority.toLowerCase()}">
                ${task.priority}
            </span>
            <button onclick="deleteTask(${task.id})"
                class="delete-btn">✕</button>
        `;
        list.appendChild(item);
    });
}

// ── Add new task ────────────────────────────────
async function addTask() {
    const input = document.getElementById("task-input");
    const title = input.value.trim();
    if (!title) return;

    await fetch(`${API}/api/tasks`, {
        method  : "POST",
        headers : { "Content-Type": "application/json" },
        body    : JSON.stringify({ title })
    });

    input.value = "";
    loadTasks();
}

// ── Toggle complete ─────────────────────────────
async function toggleTask(id, completed) {
    await fetch(`${API}/api/tasks/${id}`, {
        method  : "PUT",
        headers : { "Content-Type": "application/json" },
        body    : JSON.stringify({ completed: completed ? 1 : 0 })
    });
    loadTasks();
}

// ── Delete task ─────────────────────────────────
async function deleteTask(id) {
    await fetch(`${API}/api/tasks/${id}`, {
        method: "DELETE"
    });
    loadTasks();
}

// ── Load stats ──────────────────────────────────
async function loadStats() {
    const res  = await fetch(`${API}/api/stats`);
    const data = await res.json();

    document.getElementById("total-count").textContent     = data.total;
    document.getElementById("completed-count").textContent = data.completed;
    document.getElementById("pending-count").textContent   = data.pending;
}

// ── Allow Enter key to add task ─────────────────
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("task-input")
        .addEventListener("keydown", e => {
            if (e.key === "Enter") addTask();
        });
    loadTasks();
});