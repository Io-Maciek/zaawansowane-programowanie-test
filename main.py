from flask import Flask, request, jsonify
import uuid
from utils.task_store import tasks_lock, tasks, stop_event
from utils.processing import worker
from threading import Thread
from template import html
import requests as r
import os
from utils import process_tasking

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return html.index(queue_status())


@app.route("/queue_status", methods=["GET"])
def queue_status():
    with tasks_lock:
        processing = sum(1 for t in tasks.values() if t["status"] == 0)
    return str(processing)
    

@app.route("/get_processed_image", methods=["POST"])
@app.route("/get_processed_image/<task_id>", methods=["GET"])
def get_processed_image(task_id: None|str=None):
    if request.method == "GET":
        return process_tasking.image_processing_get_status(task_id)

    if request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "JSON body required"}), 400
        
        json_data = request.get_json()

        if not json_data or "task_ids" not in json_data:
            return {"error": "tasks list is missing"}, 400

        task_ids = json_data.get("task_ids")
        if not isinstance(task_ids, list):
            return {"error": "tasks list must be a list"}, 400
        
        return jsonify(
                process_tasking.images_processing_get_status_batch(task_ids)
                )

@app.route("/process_image", methods=["POST"])
def process_image():
    file = request.files.get("image")
    if file is None:
        return {"error": "image file missing"}, 400

    return process_tasking.image_bytes_to_task(bytes=file.read(), filename=file.filename)


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

    return process_tasking.image_bytes_to_task(bytes=image_bytes, filename=os.path.basename(url))


if __name__ == "__main__":
    _threads = []
    for i in range(2):
        t = Thread(target=worker, daemon=True, args=(f"{i}",))
        t.start()
        _threads.append(t)

    try:
        app.run(debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed, stopping workers...")
        stop_event.set()
        for t in _threads:
            t.join()
