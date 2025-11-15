import api from "../lib/api";

export async function sendPrediction(file, sensitive, budget) {
  const form = new FormData();
  form.append("img", file);
  form.append("sensitive", sensitive);
  form.append("budget", budget);

  const res = await api.post("/predict", form);
  return res.data;
}

export async function sendRegimen(file, sensitive, budget) {
  const form = new FormData();
  form.append("img", file);
  form.append("sensitive", sensitive);
  form.append("budget", budget);

  const res = await api.post("/regimen", form);
  return res.data;
}
