import axios from "axios";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json"
  }
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || "Request failed";
    return Promise.reject(new Error(message));
  }
);

export function websocketUrl(path) {
  const base = API_BASE_URL.replace(/^http/, "ws");
  return `${base}${path}`;
}
