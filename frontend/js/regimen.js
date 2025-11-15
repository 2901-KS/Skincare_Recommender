const fileReg = document.getElementById("fileReg");
const previewReg = document.getElementById("previewReg");
const generateReg = document.getElementById("generateReg");
const statusReg = document.getElementById("statusReg");
let regFile = null;

fileReg.addEventListener("change",(e)=>{
  const f = e.target.files[0];
  if(!f) return;
  regFile = f;
  previewReg.src = URL.createObjectURL(f);
  previewReg.style.display = "block";
});

generateReg.addEventListener("click", async ()=>{
  if(!regFile) return alert("Upload selfie first");
  generateReg.disabled = true; statusReg.textContent="Generating…";
  const fd = new FormData();
  fd.append("img", regFile);
  fd.append("sensitive", false);
  fd.append("budget", Number(document.getElementById("budget").value||0));
  try {
    const res = await window.api.postForm("/regimen", fd);
    localStorage.setItem("regimen_data", JSON.stringify(res));
    location.href = "regimen-result.html";
  } catch(err){
    alert("Failed: "+err.message); console.error(err);
  } finally {
    generateReg.disabled=false; statusReg.textContent="";
  }
});
