import { apiClient } from "../../../services/apiClient.js";

export const settingsService = {
  async read() {
    const { data } = await apiClient.get("/settings");
    return data;
  },
  async health() {
    const { data } = await apiClient.get("/health");
    return data;
  },
  async lookups() {
    const { data } = await apiClient.get("/settings/lookups");
    return data;
  }
};
