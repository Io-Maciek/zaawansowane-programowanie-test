from utils.task_store import task_queue, tasks, tasks_lock, stop_event
from utils import detection
import base64
import queue


def worker(process_id: str):
    while not stop_event.is_set():
        try:
            task_id, image_bytes = task_queue.get(timeout=1)
        except queue.Empty:
            continue

        print(f"\tThread '{process_id}' is processing image '{task_id}'\t({tasks[task_id]["filename"]}).")

        try:
            count, result_bytes = detection.count_crowd(image_bytes)
            encoded = base64.b64encode(result_bytes).decode("utf-8")

            with tasks_lock:
                filename = tasks[task_id]["filename"]
                tasks[task_id] = {
                    "status": 1,
                    "count": count,
                    "image_bytes": encoded,
                    "filename": "out_" + filename
                }

        except Exception as e:
            print(f"\tThread '{process_id}' encountered error\n\t{e}\n\t on image '{task_id}'\t({tasks[task_id]["filename"]}).")

            with tasks_lock:
                tasks[task_id] = {
                    "status": -1,
                    "error": str(e)
                }
        print(f"\tThread '{process_id}' succesfully processed image '{task_id}'\t({tasks[task_id]["filename"]}).")
        task_queue.task_done()

    print(f"\tThread '{process_id}' stopped.")
