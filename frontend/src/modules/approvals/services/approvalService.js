import { apiClient } from "../../../services/apiClient.js";

export const approvalService = {
  async list() {
    const { data } = await apiClient.get("/approvals");
    return data;
  },
  async pending() {
    const { data } = await apiClient.get("/approvals/pending");
    return data;
  },
  async approve(id, payload) {
    const { data } = await apiClient.post(`/approvals/${id}/approve`, payload);
    return data;
  },
  async reject(id, payload) {
    const { data } = await apiClient.post(`/approvals/${id}/reject`, payload);
    return data;
  }
};
