from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

task_list = []


@app.route("/")
def index():
    current_tasks = task_list
    return render_template("index.html", current_tasks=current_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    t = request.form.get("task_input", "").strip()

    if t:
        task_list.append({"text": t, "done": False})

    return redirect(url_for("index"))


@app.route("/complete/<int:idx>", methods=["POST"])
def complete_task(idx):
    if 0 <= idx < len(task_list):
        task_list[idx]["done"] = not task_list[idx]["done"]
    return redirect(url_for("index"))


@app.route("/delete/<int:idx>", methods=["POST"])
def delete_task(idx):
    if 0 <= idx < len(task_list):
        task_list.pop(idx)
    return redirect(url_for("index"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)

# TODO: Add a database to store tasks (tasks reset when server restarts)
