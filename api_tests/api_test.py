import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

API_URL = "http://127.0.0.1:5000"
DATA_DIR = "data"


def timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


# wysyla plik do api ze sciezki
def upload_image(path: str) -> tuple[str, str]:
    with open(path, "rb") as f:
        files = {"image": f}
        resp = requests.post(f"{API_URL}/process_image", files=files)
        task_id = resp.json()["task_id"]
        return task_id, os.path.basename(path)


# zapytanie GET do statusu zdjecia i/lub jego wyniku
def get_task_status_result(task_id: str) -> dict: return requests.get(f"{API_URL}/get_processed_image/{task_id}").json()


if __name__ == "__main__":

    # pobiera zdjecia z data
    images = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"Found {len(images)} images")

    # wyslanie wszystkich obrazkow do api w 4 wątkach, agalogincze do for _ in (range): Thread(...).start()
    pending = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_image, img) for img in images]

        for future in as_completed(futures):
            task_id, filename = future.result()
            pending[task_id] = {"filename": filename, "status": 0}
            print(f"[{timestamp()}]\tUploaded {filename} → task_id={task_id}")

    # pobieranie wyliczonych zdjec i oczekiwanie na tego jeszcze nie gotowe
    total_images = len(pending)
    completed_count = 0

    while completed_count < total_images:
        for task_id in list(pending.keys()):

            response = get_task_status_result(task_id)
            if response["status"] == 1:
                completed_count += 1
                print(f"[{timestamp()}]\tDONE {pending[task_id]['filename']} - count={response['count']} ({completed_count}/{total_images})")
                del pending[task_id]
            elif response["status"] == -1:
                completed_count += 1
                print(f"[{timestamp()}]\tX ERROR {pending[task_id]['filename']} - {response['error']} ({completed_count}/{total_images})")
                del pending[task_id]

        time.sleep(1.0)  # sleep, aby nie wysylac za duzo zapytan do API

    print(f"\n[{timestamp()}]\tAll tasks completed: {total_images}")
