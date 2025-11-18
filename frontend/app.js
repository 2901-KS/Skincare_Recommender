// app.js - shared helpers
const BASE_URL = 'http://127.0.0.1:8000';

// helper to show toast-ish message
function showMessage(text, timeout = 3000){
  const el = document.createElement('div');
  el.textContent = text;
  Object.assign(el.style, {
    position: 'fixed', right: '18px', bottom: '18px', background: '#6b2b5a', color:'#fff',
    padding:'10px 14px', borderRadius:'10px', boxShadow:'0 8px 20px rgba(0,0,0,0.15)', zIndex:9999
  });
  document.body.appendChild(el);
  setTimeout(()=> el.remove(), timeout);
}

// store response in session storage then navigate
function storeAndNavigate(key, data, target){
  sessionStorage.setItem(key, JSON.stringify(data));
  window.location.href = target;
}

// pretty print JSON into an element
function prettyJSON(el, obj){
  el.innerHTML = '';
  try {
    const formatted = JSON.stringify(obj, null, 2);
    const pre = document.createElement('pre');
    pre.className = 'json';
    pre.textContent = formatted;
    el.appendChild(pre);
  } catch(e){
    el.textContent = 'Could not format JSON.';
  }
}
