import { apiClient, websocketUrl } from "../../../services/apiClient.js";

export const executionService = {
  async samples() {
    const { data } = await apiClient.get("/governance/samples");
    return data;
  },
  liveSocketUrl() {
    return websocketUrl("/ws/governance/live");
  }
};
