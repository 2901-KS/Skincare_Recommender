// central API helper
const BASE = "http://127.0.0.1:8000";

async function postForm(path, formData) {
  try {
    const res = await fetch(BASE + path, {
      method: "POST",
      body: formData
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`${res.status} ${res.statusText} - ${txt}`);
    }
    return await res.json();
  } catch (err) {
    console.error("API error:", err);
    throw err;
  }
}

// export for other files
window.api = { postForm };
