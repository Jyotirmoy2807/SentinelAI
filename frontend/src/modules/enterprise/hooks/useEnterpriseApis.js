import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { enterpriseService } from "../services/enterpriseService.js";
import { GOVERNANCE_LOOKUPS_QUERY_KEY } from "../../governance/hooks/useGovernanceResources.js";

export function useEnterpriseApis() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["enterprise"], queryFn: enterpriseService.list });
  const lookups = useQuery({ queryKey: ["enterprise-lookups"], queryFn: enterpriseService.lookups });
  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["enterprise"] });
    queryClient.invalidateQueries({ queryKey: ["enterprise-lookups"] });
    queryClient.invalidateQueries({ queryKey: GOVERNANCE_LOOKUPS_QUERY_KEY });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };
  return {
    ...query,
    lookups,
    createApi: useMutation({ mutationFn: enterpriseService.create, onSuccess: invalidate }),
    updateApi: useMutation({ mutationFn: ({ id, payload }) => enterpriseService.update(id, payload), onSuccess: invalidate }),
    activateApi: useMutation({ mutationFn: enterpriseService.activate, onSuccess: invalidate }),
    deactivateApi: useMutation({ mutationFn: enterpriseService.deactivate, onSuccess: invalidate }),
    deleteApi: useMutation({ mutationFn: enterpriseService.remove, onSuccess: invalidate })
  };
}
