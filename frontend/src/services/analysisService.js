import { apiRequest } from "./api.js";

export function analyzeFace(formData) {
  return apiRequest("/analyze-face", {
    method: "POST",
    body: formData,
  });
}

export function getHistory() {
  return apiRequest("/history");
}

export function deleteHistoryItem(id) {
  return apiRequest(`/history/${id}`, { method: "DELETE" });
}
