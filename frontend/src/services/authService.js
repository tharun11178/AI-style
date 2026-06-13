import { apiRequest, clearToken, setToken } from "./api.js";

export async function login(credentials) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
  setToken(data.token);
  return data.user;
}

export async function registerAccount(payload) {
  const data = await apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  setToken(data.token);
  return data.user;
}

export function getCurrentUser() {
  return apiRequest("/auth/me");
}

export async function logout() {
  await apiRequest("/auth/logout", { method: "POST" }).catch(() => null);
  clearToken();
}
