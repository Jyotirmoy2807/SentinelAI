import { apiClient } from "../../../services/apiClient.js";

export const auditService = {
  async list() {
    const { data } = await apiClient.get("/audit");
    return data;
  },
  async detail(requestId) {
    const { data } = await apiClient.get(`/audit/${requestId}`);
    return data;
  }
};
