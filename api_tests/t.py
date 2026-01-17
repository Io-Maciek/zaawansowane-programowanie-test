import requests

API_URL = "http://127.0.0.1:5000"
DATA_DIR = "data"

resp = requests.post(
    f"{API_URL}/process_image_url",
    json={"url": "https://universo.salonline.com.br/wp-content/uploads/2018/05/selfie-perfeita.jpg"})

print(resp.json())

# potem: http://127.0.0.1:5000/get_processed_image/
