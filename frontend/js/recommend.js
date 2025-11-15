// recommend page logic
const fileInput = document.getElementById("fileInput");
const previewImg = document.getElementById("previewImg");
const analyzeBtn = document.getElementById("analyzeBtn");
const status = document.getElementById("status");

let pickedFile = null;
fileInput.addEventListener("change", (e) => {
  const f = e.target.files[0];
  if (!f) return;
  pickedFile = f;
  previewImg.src = URL.createObjectURL(f);
  previewImg.style.display = "block";
});

analyzeBtn.addEventListener("click", async () => {
  if (!pickedFile) return alert("Please upload a selfie first.");
  status.textContent = "Processing…";
  analyzeBtn.disabled = true;

  const fd = new FormData();
  fd.append("img", pickedFile);
  fd.append("sensitive", document.getElementById("sensitive").value);
  fd.append("budget", 0);

  try {
    const data = await window.api.postForm("/predict", fd);
    // store and navigate
    localStorage.setItem("recommend_data", JSON.stringify(data));
    location.href = "recommend-result.html";
  } catch (err) {
    alert("Analysis failed: " + (err.message||err));
    console.error(err);
  } finally {
    analyzeBtn.disabled = false;
    status.textContent = "";
  }
});
