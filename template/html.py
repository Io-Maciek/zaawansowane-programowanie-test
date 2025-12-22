def index() -> str:
    return """
<!doctype html>
<title>Liczenie osób</title>

<h1>Dodaj zdjęcie</h1>

<form id="uploadForm" enctype="multipart/form-data">
  <input type="file" name="image" id="imageInput" required>
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

  const formData = new FormData(form);

  const res = await fetch("/process_image", {
    method: "POST",
    body: formData
  });

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

    console.log(data.filename);
      resultFilename = data.filename;

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
console.log(resultFilename);
  const a = document.createElement("a");
  a.href = resultImage.src;
  a.download = resultFilename;
  a.click();
}
</script>
"""
