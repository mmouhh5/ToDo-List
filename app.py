import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

TASKS_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)


@app.route("/")
def index():
    current_tasks = load_tasks()
    return render_template("index.html", current_tasks=current_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    t = request.form.get("task_input", "").strip()

    if t:
        tasks = load_tasks()
        tasks.append({"text": t, "done": False})
        save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/complete/<int:idx>", methods=["POST"])
def complete_task(idx):
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = not tasks[idx]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:idx>", methods=["POST"])
def delete_task(idx):
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
