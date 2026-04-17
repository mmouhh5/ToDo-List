import json
import os
import time
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
    sort_by = request.args.get("sort")
    filter_by = request.args.get("filter")
    current_tasks = load_tasks()
    
    # temporary fix to keep indexes matched - just sort and save it!
    if sort_by == "new":
        current_tasks.sort(key=lambda x: x.get("date", ""), reverse=True)
        save_tasks(current_tasks)
    elif sort_by == "old":
        current_tasks.sort(key=lambda x: x.get("date", ""))
        save_tasks(current_tasks)

    return render_template("index.html", current_tasks=current_tasks, filter_by=filter_by)


@app.route("/add", methods=["POST"])
def add_task():
    t = request.form.get("task_input", "").strip()

    if t:
        tasks = load_tasks()
        d = str(time.time())
        tasks.append({"text": t, "done": False, "date": d})
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
