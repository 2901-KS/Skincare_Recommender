const checkBtn = document.getElementById("checkBtn");
const ingredientText = document.getElementById("ingredientText");
const ingredientResult = document.getElementById("ingredientResult");

checkBtn.addEventListener("click", async ()=>{
  const text = ingredientText.value.trim();
  if(!text) return alert("Paste ingredient list first");
  checkBtn.disabled = true; ingredientResult.innerHTML = "Analyzing…";
  const fd = new FormData();
  fd.append("ingredients", text);
  fd.append("acne_level", 2);
  fd.append("skin_type", 1);
  fd.append("skin_tone", 1);
  fd.append("sensitive", false);

  try {
    const res = await window.api.postForm("/ingredient-check", fd);
    ingredientResult.innerHTML = `<pre style="white-space:pre-wrap">${JSON.stringify(res.analysis, null, 2)}</pre>`;
  } catch(err){
    ingredientResult.innerHTML = `<div class="small">Error: ${err.message}</div>`;
  } finally {
    checkBtn.disabled=false;
  }
});
