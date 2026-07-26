import { apiClient } from "../../../services/apiClient.js";

export const agentService = {
  async list() {
    const { data } = await apiClient.get("/agents");
    return data;
  },
  async create(payload) {
    const { data } = await apiClient.post("/agents", payload);
    return data;
  },
  async update(id, payload) {
    const { data } = await apiClient.put(`/agents/${id}`, payload);
    return data;
  },
  async suspend(id) {
    const { data } = await apiClient.post(`/agents/${id}/suspend`);
    return data;
  },
  async activate(id) {
    const { data } = await apiClient.post(`/agents/${id}/activate`);
    return data;
  },
  async block(id) {
    const { data } = await apiClient.post(`/agents/${id}/block`);
    return data;
  },
  async remove(id) {
    const { data } = await apiClient.delete(`/agents/${id}`);
    return data;
  }
};
