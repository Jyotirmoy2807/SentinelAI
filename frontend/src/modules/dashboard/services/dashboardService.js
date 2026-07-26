import { apiClient } from "../../../services/apiClient.js";

export const dashboardService = {
  async summary() {
    const { data } = await apiClient.get("/dashboard");
    return data;
  }
};
