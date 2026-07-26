import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { enterpriseService } from "../services/enterpriseService.js";

export function useEnterpriseApis() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["enterprise"], queryFn: enterpriseService.list });
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["enterprise"] });
  return {
    ...query,
    createApi: useMutation({ mutationFn: enterpriseService.create, onSuccess: invalidate }),
    updateApi: useMutation({ mutationFn: ({ id, payload }) => enterpriseService.update(id, payload), onSuccess: invalidate }),
    activateApi: useMutation({ mutationFn: enterpriseService.activate, onSuccess: invalidate }),
    deactivateApi: useMutation({ mutationFn: enterpriseService.deactivate, onSuccess: invalidate }),
    deleteApi: useMutation({ mutationFn: enterpriseService.remove, onSuccess: invalidate })
  };
}
