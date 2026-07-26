import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { governanceService } from "../services/governanceService.js";

export const GOVERNANCE_LOOKUPS_QUERY_KEY = ["governance-lookups"];

export function useGovernanceResources() {
  const queryClient = useQueryClient();
  const invalidatePolicies = () => {
    queryClient.invalidateQueries({ queryKey: ["governance-policies"] });
    queryClient.invalidateQueries({ queryKey: ["budget-policies"] });
    queryClient.invalidateQueries({ queryKey: ["policy-deployment"] });
    queryClient.invalidateQueries({ queryKey: ["policy-history"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    queryClient.invalidateQueries({ queryKey: GOVERNANCE_LOOKUPS_QUERY_KEY });
  };

  const [governancePolicies, budgetPolicies, settings, lookups, deployment, history] = useQueries({
    queries: [
      { queryKey: ["governance-policies"], queryFn: governanceService.listGovernancePolicies },
      { queryKey: ["budget-policies"], queryFn: governanceService.listBudgetPolicies },
      { queryKey: ["settings"], queryFn: governanceService.settings },
      { queryKey: GOVERNANCE_LOOKUPS_QUERY_KEY, queryFn: governanceService.lookups },
      { queryKey: ["policy-deployment"], queryFn: governanceService.latestDeployment },
      { queryKey: ["policy-history"], queryFn: governanceService.history }
    ]
  });

  return {
    governancePolicies,
    budgetPolicies,
    settings,
    lookups,
    deployment,
    history,
    compareVersions: (left, right) => queryClient.fetchQuery({ queryKey: ["policy-compare", left, right], queryFn: () => governanceService.compare(left, right) }),
    createGovernancePolicy: useMutation({ mutationFn: governanceService.createGovernancePolicy, onSuccess: invalidatePolicies }),
    updateGovernancePolicy: useMutation({ mutationFn: ({ id, payload }) => governanceService.updateGovernancePolicy(id, payload), onSuccess: invalidatePolicies }),
    deleteGovernancePolicy: useMutation({ mutationFn: governanceService.deleteGovernancePolicy, onSuccess: invalidatePolicies }),
    duplicateGovernancePolicy: useMutation({ mutationFn: governanceService.duplicateGovernancePolicy, onSuccess: invalidatePolicies }),
    setGovernancePolicyEnabled: useMutation({ mutationFn: governanceService.setGovernancePolicyEnabled, onSuccess: invalidatePolicies }),
    createBudgetPolicy: useMutation({ mutationFn: governanceService.createBudgetPolicy, onSuccess: invalidatePolicies }),
    updateBudgetPolicy: useMutation({ mutationFn: ({ id, payload }) => governanceService.updateBudgetPolicy(id, payload), onSuccess: invalidatePolicies }),
    deleteBudgetPolicy: useMutation({ mutationFn: governanceService.deleteBudgetPolicy, onSuccess: invalidatePolicies }),
    duplicateBudgetPolicy: useMutation({ mutationFn: governanceService.duplicateBudgetPolicy, onSuccess: invalidatePolicies }),
    setBudgetPolicyStatus: useMutation({ mutationFn: governanceService.setBudgetPolicyStatus, onSuccess: invalidatePolicies }),
    deploy: useMutation({ mutationFn: governanceService.deploy, onSuccess: invalidatePolicies }),
    restore: useMutation({ mutationFn: governanceService.restore, onSuccess: invalidatePolicies })
  };
}
