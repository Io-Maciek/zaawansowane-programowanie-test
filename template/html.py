def index() -> str:
    return """
<!doctype html>
<title>Liczenie osób</title>

<h1>Dodaj zdjęcie</h1>

<form id="uploadForm" enctype="multipart/form-data">
  <label>Wybierz plik: 
    <input type="file" name="image" id="imageInput">
  </label>
  <label>Lub wpisz link do obrazu: 
    <input type="text" name="image_url" id="imageUrlInput" placeholder="https://example.com/image.jpg">
  </label>

  <br>
  <button type="submit" id="submitBtn">Wyślij</button>
</form>

<p id="status"></p>

<div id="resultContainer" style="display:none;">
  <hr>
  <h2>Wykryto osób: <span id="count"></span></h2>

  <img id="resultImage" style="max-width:600px">

  <br><br>
  <button onclick="download()">DOWNLOAD</button>
</div>

<script>
let resultFilename = "out_result.jpg";  // domyślna
const form = document.getElementById("uploadForm");
const submitBtn = document.getElementById("submitBtn");
const statusEl = document.getElementById("status");
const resultContainer = document.getElementById("resultContainer");
const countEl = document.getElementById("count");
const resultImage = document.getElementById("resultImage");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    countEl.innerText = "";
    resultImage.src = "";
    resultContainer.style.display = "none";

    submitBtn.disabled = true;
    statusEl.innerText = "Wysyłanie obrazu...";

    const file = document.getElementById("imageInput").files[0];
    const url = document.getElementById("imageUrlInput").value.trim();

    let res;

    if (file) {
        // Wysyłamy plik
        const formData = new FormData();
        formData.append("image", file);

        res = await fetch("/process_image", {
            method: "POST",
            body: formData
        });

    } else if (url) {
        // Wysyłamy URL w JSON
        res = await fetch("/process_image_url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });

    } else {
        alert("Proszę wybrać plik lub wpisać link do obrazu");
        submitBtn.disabled = false;
        return;
    }

    const data = await res.json();
    statusEl.innerText = "Przetwarzanie obrazu...";

    pollStatus(data.task_id);
});

function pollStatus(taskId) {
    const interval = setInterval(async () => {
        const res = await fetch(`/get_processed_image/${taskId}`);
        const data = await res.json();

        if (data.status === 0) {
            statusEl.innerText = "Przetwarzanie obrazu...";
        }

        if (data.status === 1) {
            clearInterval(interval);
            resultFilename = data.filename;
            document.getElementById("imageInput").value = "";
            document.getElementById("imageUrlInput").value = "";
            

            statusEl.innerText = "Gotowe!";
            countEl.innerText = data.count;
            resultImage.src = "data:image/jpeg;base64," + data.image_bytes;
            resultContainer.style.display = "block";
            submitBtn.disabled = false;
        }

        if (data.status === -1) {
            clearInterval(interval);
            statusEl.innerText = "Błąd: " + data.error;
            submitBtn.disabled = false;
        }
    }, 1000);
}

function download() {
    const a = document.createElement("a");
    a.href = resultImage.src;
    a.download = resultFilename;
    a.click();
}
</script>
"""
