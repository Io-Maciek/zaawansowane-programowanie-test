from flask import Flask, request
import uuid
from utils.task_store import task_queue, tasks
from utils.processing import worker
from threading import Thread
from template import html
import requests as r
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return html.index()


@app.route("/process_image", methods=["POST"])
def process_image():
    file = request.files["image"]
    filename = file.filename

    if file is None:
        return {"error": "image file missing"}, 400

    image_bytes = file.read()

    task_id = str(uuid.uuid4())

    tasks[task_id] = {"status": 0, "filename": filename}
    task_queue.put((task_id, image_bytes))

    return {"task_id": task_id}, 202


@app.route("/get_processed_image/<task_id>", methods=["GET"])
def get_processed_image(task_id):
    task = tasks.get(task_id)

    if task is None:
        return {"error": "task not found", "status": -1}, 404

    if task["status"] == 0:
        return {"status": 0}

    elif task["status"] != 1:
        # też warto usunąć
        result = {
            "status": -1,
            "error": task.get("error", "unknown error")
        }
        del tasks[task_id]
        return result

    # status == 1
    result = {
        "status": 1,
        "count": task["count"],
        "image_bytes": task["image_bytes"],
        "filename": task["filename"]
    }

    del tasks[task_id]

    return result


@app.route("/process_image_url", methods=["POST"])
def process_image_url():
    json_data = request.get_json()
    if not json_data or "url" not in json_data:
        return {"error": "url missing"}, 400

    url = json_data["url"]
    try:
        resp = r.get(url)
        resp.raise_for_status()
        image_bytes = resp.content
    except Exception as e:
        return {"error": f"failed to download image: {e}"}, 400

    filename = os.path.basename(url)
    task_id = str(uuid.uuid4())

    tasks[task_id] = {"status": 0, "filename": filename}
    task_queue.put((task_id, image_bytes))

    return {"task_id": task_id}, 202


if __name__ == "__main__":
    thread = Thread(target=worker, daemon=True)
    thread.start()

    app.run()
# todo: download 1000 photos of people, run those throuth the api
