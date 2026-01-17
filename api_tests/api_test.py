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
    with requests.Session() as session:
        with open(path, "rb") as f:
            files = {"image": f}
            resp = session.post(
                f"{API_URL}/process_image",
                files=files,
                timeout=(3, 30)
            )
            resp.raise_for_status()
            task_id = resp.json()["task_id"]
            return task_id, os.path.basename(path)


# zapytanie GET do statusu zdjecia i/lub jego wyniku
def get_task_status_result(task_id: str, session: requests.Session) -> dict: return session.get(f"{API_URL}/get_processed_image/{task_id}", timeout=(3, 30)).json()


def get_tasks_status_batch(
    tasks_ids: list[str],
    session: requests.Session
) -> dict[str, dict]:
    return session.post(
        f"{API_URL}/get_processed_image",
        json={"task_ids": tasks_ids},
        timeout=(3, 60)
    ).json()


if __name__ == "__main__":
    session = requests.Session()

    # pobiera zdjecia z data
    images = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]  # [0:200]

    print(f"Found {len(images)} images")

    # wyslanie wszystkich obrazkow do api w 4 wątkach, agalogincze do for _ in (range): Thread(...).start()
    pending = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_image, img) for img in images]

        for future in as_completed(futures):
            task_id, filename = future.result()
            pending[task_id] = {"filename": filename, "status": 0}
            print(f"[{timestamp()}]\tUploaded {filename} -> task_id={task_id}")

    # pobieranie wyliczonych zdjec (batch)
    total_images = len(pending)
    completed_count = 0

    BATCH_SIZE = 50      # zabezpieczenie na duże odpowiedzi
    SLEEP_TIME = 1.0

    while completed_count < total_images:
        task_ids = list(pending.keys())

        # dzielimy na mniejsze batche
        for i in range(0, len(task_ids), BATCH_SIZE):
            batch_ids = task_ids[i:i + BATCH_SIZE]

            try:
                responses = get_tasks_status_batch(batch_ids, session)
            except Exception as e:
                print(f"[{timestamp()}]\tBATCH ERROR: {e}")
                continue

            for task_id, response in responses.items():
                filename = pending[task_id]["filename"]

                status = response.get("status")
                if status == 0:
                    continue

                if status == 1:
                    completed_count += 1
                    print(
                        f"[{timestamp()}]\tDONE {filename} "
                        f"- count={response['count']} "
                        f"({completed_count}/{total_images})"
                    )
                    del pending[task_id]
                    continue

                if status == -1:
                    completed_count += 1
                    error = response.get("error", "unknown error")
                    print(
                        f"[{timestamp()}]\tX ERROR {filename} "
                        f"- {error} "
                        f"({completed_count}/{total_images})"
                    )
                    del pending[task_id]

        time.sleep(SLEEP_TIME)

    print(f"\n[{timestamp()}]\tAll tasks completed: {total_images}")


if __name__ == "__main__NOT":
    session = requests.Session()

    # pobiera zdjecia z data
    images = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ][0:200]

    print(f"Found {len(images)} images")

    # wyslanie wszystkich obrazkow do api w 4 wątkach, agalogincze do for _ in (range): Thread(...).start()
    pending = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_image, img) for img in images]

        for future in as_completed(futures):
            task_id, filename = future.result()
            pending[task_id] = {"filename": filename, "status": 0}
            print(f"[{timestamp()}]\tUploaded {filename} -> task_id={task_id}")

    # pobieranie wyliczonych zdjec i oczekiwanie na tego jeszcze nie gotowe
    total_images = len(pending)
    completed_count = 0

    while completed_count < total_images:
        for task_id in list(pending.keys()):

            response = get_task_status_result(task_id, session)
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
