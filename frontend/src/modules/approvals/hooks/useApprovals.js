import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { approvalService } from "../services/approvalService.js";

export function useApprovals() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["approvals"], queryFn: approvalService.list, refetchInterval: 10000 });
  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["approvals"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    queryClient.invalidateQueries({ queryKey: ["audit"] });
  };
  return {
    ...query,
    approveApproval: useMutation({ mutationFn: ({ id, payload }) => approvalService.approve(id, payload), onSuccess: invalidate }),
    rejectApproval: useMutation({ mutationFn: ({ id, payload }) => approvalService.reject(id, payload), onSuccess: invalidate })
  };
}
