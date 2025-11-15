const compareBtn = document.getElementById("compareBtn");
const prod1 = document.getElementById("prod1");
const prod2 = document.getElementById("prod2");
const compareResult = document.getElementById("compareResult");

compareBtn.addEventListener("click", async ()=>{
  const a = prod1.value.trim();
  const b = prod2.value.trim();
  if(!a||!b) return alert("Enter both product names");
  compareBtn.disabled = true; compareResult.innerHTML="Comparing…";
  const fd = new FormData();
  fd.append("product1", a);
  fd.append("product2", b);
  fd.append("acne_level", 2);
  fd.append("skin_type", 1);
  fd.append("skin_tone", 1);
  fd.append("sensitive", false);

  try {
    const res = await window.api.postForm("/compare-products", fd);
    compareResult.innerHTML = `<pre style="white-space:pre-wrap">${JSON.stringify(res.comparison, null, 2)}</pre>`;
  } catch(err){
    compareResult.innerHTML = `<div class="small">Error: ${err.message}</div>`;
  } finally {
    compareBtn.disabled = false;
  }
});
