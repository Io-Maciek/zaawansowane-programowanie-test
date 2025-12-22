from flask import Flask, request, render_template_string, send_file
from utils import detection
from io import BytesIO
import uuid
import base64
from utils.task_store import task_queue, tasks
from utils.processing import worker
from threading import Thread
from template import html

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
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


if __name__ == "__main__":
    thread = Thread(target=worker, daemon=True)
    thread.start()

    app.run()
