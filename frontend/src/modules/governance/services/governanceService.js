import { apiClient } from "../../../services/apiClient.js";

const endpoints = {
  policies: "/policies",
  firewall: "/firewall",
  compliance: "/compliance",
  budget: "/budget"
};

export const governanceService = {
  async list(kind) {
    const { data } = await apiClient.get(endpoints[kind]);
    return data;
  },
  async create(kind, payload) {
    const { data } = await apiClient.post(endpoints[kind], payload);
    return data;
  },
  async update(kind, id, payload) {
    const { data } = await apiClient.put(`${endpoints[kind]}/${id}`, payload);
    return data;
  },
  async remove(kind, id) {
    const { data } = await apiClient.delete(`${endpoints[kind]}/${id}`);
    return data;
  }
};
