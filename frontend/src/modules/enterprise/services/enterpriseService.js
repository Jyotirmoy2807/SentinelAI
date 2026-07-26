import { apiClient } from "../../../services/apiClient.js";

export const enterpriseService = {
  async list() {
    const { data } = await apiClient.get("/enterprise");
    return data;
  },
  async lookups() {
    const { data } = await apiClient.get("/enterprise/lookups");
    return data;
  },
  async create(payload) {
    const { data } = await apiClient.post("/enterprise", payload);
    return data;
  },
  async update(id, payload) {
    const { data } = await apiClient.put(`/enterprise/${id}`, payload);
    return data;
  },
  async activate(id) {
    const { data } = await apiClient.post(`/enterprise/${id}/activate`);
    return data;
  },
  async deactivate(id) {
    const { data } = await apiClient.post(`/enterprise/${id}/deactivate`);
    return data;
  },
  async remove(id) {
    const { data } = await apiClient.delete(`/enterprise/${id}`);
    return data;
  }
};
