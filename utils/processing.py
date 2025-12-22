from utils.task_store import task_queue, tasks
from utils import detection
import base64

def worker():
    while True:
        task_id, image_bytes = task_queue.get()

        try:
            count, result_bytes = detection.count_crowd(image_bytes)

            tasks[task_id] = {
                "status": 1,
                "count": count,
                "image_bytes": base64.b64encode(result_bytes).decode("utf-8"),
                "filename": "out_"+tasks[task_id]["filename"]
            }

        except Exception as e:
            tasks[task_id] = {
                "status": -1,
                "error": str(e)
            }

        task_queue.task_done()