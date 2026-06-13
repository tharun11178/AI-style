import { apiRequest } from "./api.js";

export function getHairstyleRecommendations() {
  return apiRequest("/recommend/hairstyle");
}

export function getOutfitRecommendations() {
  return apiRequest("/recommend/outfits");
}

export function getColorRecommendations() {
  return apiRequest("/recommend/colors");
}

export function saveFeedback(payload) {
  return apiRequest("/feedback", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getAdminAnalytics() {
  return apiRequest("/admin/analytics");
}

export function getAdminUsers() {
  return apiRequest("/admin/users");
}
