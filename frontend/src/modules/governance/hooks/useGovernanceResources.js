import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { governanceService } from "../services/governanceService.js";

export function useGovernanceResources() {
  const queryClient = useQueryClient();
  const [policies, firewall, compliance, budget] = useQueries({
    queries: ["policies", "firewall", "compliance", "budget"].map((kind) => ({
      queryKey: [kind],
      queryFn: () => governanceService.list(kind)
    }))
  });
  const invalidate = (kind) => queryClient.invalidateQueries({ queryKey: [kind] });
  return {
    policies,
    firewall,
    compliance,
    budget,
    createResource: useMutation({
      mutationFn: ({ kind, payload }) => governanceService.create(kind, payload),
      onSuccess: (_, variables) => invalidate(variables.kind)
    }),
    updateResource: useMutation({
      mutationFn: ({ kind, id, payload }) => governanceService.update(kind, id, payload),
      onSuccess: (_, variables) => invalidate(variables.kind)
    }),
    deleteResource: useMutation({
      mutationFn: ({ kind, id }) => governanceService.remove(kind, id),
      onSuccess: (_, variables) => invalidate(variables.kind)
    })
  };
}
