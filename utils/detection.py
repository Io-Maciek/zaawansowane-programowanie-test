import cv2
import numpy as np
from utils import model

def count_crowd(image_bytes: bytes, threshold=0.3):
    # bytes -> numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # decode JPEG/PNG
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Nie można zdekodować obrazu")

    rows, cols = img.shape[:2]
    net = model.get_model()

    blob = cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    out = net.forward()

    count = 0
    for detection in out[0, 0, :, :]:
        score = float(detection[2])
        class_id = int(detection[1])
        if score > threshold and class_id == 1:
            count += 1
            left = int(detection[3] * cols)
            top = int(detection[4] * rows)
            right = int(detection[5] * cols)
            bottom = int(detection[6] * rows)
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    # obraz wynikowy -> bytes
    ok, buffer = cv2.imencode(".jpg", img)
    if not ok:
        raise RuntimeError("Nie udało się zakodować obrazu")

    return count, buffer.tobytes()
