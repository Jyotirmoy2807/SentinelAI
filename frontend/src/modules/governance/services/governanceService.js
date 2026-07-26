import { apiClient } from "../../../services/apiClient.js";

const endpoints = {
  policies: "/policies",
  settings: "/settings"
};

export const governanceService = {
  async list(kind) {
    const { data } = await apiClient.get(endpoints[kind]);
    return data;
  },
  async settings() {
    const { data } = await apiClient.get(endpoints.settings);
    return data;
  },
};
