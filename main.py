from flask import Flask, request, render_template_string, send_file
from utils import detection
from io import BytesIO
import uuid
import base64

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Liczenie osób</title>

<h1>Dodaj zdjęcie</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="image" required>
  <button type="submit">Wyślij</button>
</form>

{% if count %}
<hr>
<h2>Wykryto osób: {{ count }}</h2>

<img id="result"  src='data:image/jpeg;base64,{{ image_bytes }}' style="max-width:600px">>

<br><br>
<button onclick="download()">DOWNLOAD</button>

<script>
function download() {
  const a = document.createElement("a");
  a.href = document.getElementById("result").src;
  a.download = "result.jpg";
  a.click();
}
</script>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        filename = file.filename
        image_bytes = file.read()
        uid = str(uuid.uuid4())

        count, result_bytes = detection.count_crowd(image_bytes)

        return render_template_string(HTML, count=count, id=uid, image_bytes = base64.b64encode(result_bytes).decode("utf-8"))

    return render_template_string(HTML, count=None)


if __name__ == "__main__":
    app.run(debug=True)
