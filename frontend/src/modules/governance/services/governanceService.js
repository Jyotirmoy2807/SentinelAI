import { apiClient } from "../../../services/apiClient.js";

export const governanceService = {
  async listGovernancePolicies() {
    const { data } = await apiClient.get("/policies/governance");
    return data;
  },
  async createGovernancePolicy(payload) {
    const { data } = await apiClient.post("/policies/governance", payload);
    return data;
  },
  async updateGovernancePolicy(id, payload) {
    const { data } = await apiClient.put(`/policies/governance/${id}`, payload);
    return data;
  },
  async deleteGovernancePolicy(id) {
    await apiClient.delete(`/policies/governance/${id}`);
  },
  async duplicateGovernancePolicy(id) {
    const { data } = await apiClient.post(`/policies/governance/${id}/duplicate`);
    return data;
  },
  async setGovernancePolicyEnabled({ id, enabled }) {
    const { data } = await apiClient.post(`/policies/governance/${id}/${enabled ? "enable" : "disable"}`);
    return data;
  },
  async listBudgetPolicies() {
    const { data } = await apiClient.get("/policies/budgets");
    return data;
  },
  async createBudgetPolicy(payload) {
    const { data } = await apiClient.post("/policies/budgets", payload);
    return data;
  },
  async updateBudgetPolicy(id, payload) {
    const { data } = await apiClient.put(`/policies/budgets/${id}`, payload);
    return data;
  },
  async deleteBudgetPolicy(id) {
    await apiClient.delete(`/policies/budgets/${id}`);
  },
  async duplicateBudgetPolicy(id) {
    const { data } = await apiClient.post(`/policies/budgets/${id}/duplicate`);
    return data;
  },
  async setBudgetPolicyStatus({ id, active }) {
    const { data } = await apiClient.post(`/policies/budgets/${id}/${active ? "activate" : "deactivate"}`);
    return data;
  },
  async deploy() {
    const { data } = await apiClient.post("/policies/deploy");
    return data;
  },
  async latestDeployment() {
    const { data } = await apiClient.get("/policies/deployments/latest");
    return data;
  },
  async history() {
    const { data } = await apiClient.get("/policies/history");
    return data;
  },
  async compare(left, right) {
    const { data } = await apiClient.get("/policies/history/compare", { params: { left, right } });
    return data;
  },
  async restore(versionId) {
    const { data } = await apiClient.post(`/policies/history/${versionId}/restore`);
    return data;
  },
  async lookups() {
    const { data } = await apiClient.get("/settings/lookups");
    return data;
  },
  async settings() {
    const { data } = await apiClient.get("/settings");
    return data;
  }
};
