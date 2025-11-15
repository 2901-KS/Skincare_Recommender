import api from "../lib/api";

export async function checkIngredients(data) {
  const form = new FormData();
  Object.entries(data).forEach(([k, v]) => form.append(k, v));

  const res = await api.post("/ingredient-check", form);
  return res.data;
}

export async function compareProducts(data) {
  const form = new FormData();
  Object.entries(data).forEach(([k, v]) => form.append(k, v));

  const res = await api.post("/compare-products", form);
  return res.data;
}
