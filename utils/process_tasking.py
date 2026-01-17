from utils.task_store import task_queue, tasks, tasks_lock, stop_event
import uuid


def image_bytes_to_task(bytes, filename: str):
    task_id = str(uuid.uuid4())

    with tasks_lock:
        tasks[task_id] = {
            "status": 0,
            "filename": filename
        }

    task_queue.put((task_id, bytes))
    return {"task_id": task_id}, 202


def image_processing_get_status(task_id: str) -> dict:
    with tasks_lock:
        task = tasks.get(task_id)

        if task is None:
            return {"error": "task not found", "status": -1}, 404

        if task["status"] == 0:
            return {"status": 0}

        if task["status"] != 1:
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


def images_processing_get_status_batch(tasks_ids: list[str]) -> dict:
    result = {}
    with tasks_lock:
        for task_id in tasks_ids:
            task = tasks.get(task_id)

            if task is None:
                result[task_id] = {"error": "task not found", "status": -1}
                continue

            if task["status"] == 0:
                result[task_id] = {"status": 0}
                continue

            if task["status"] != 1:
                result[task_id] = {
                    "status": -1,
                    "error": task.get("error", "unknown error")
                }
                del tasks[task_id]
                continue

            # status == 1
            result[task_id] = {
                "status": 1,
                "count": task["count"],
                # "image_bytes": task["image_bytes"],
                "filename": task["filename"]
            }
            del tasks[task_id]

    return result
