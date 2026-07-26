import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { agentService } from "../services/agentService.js";

export function useAgents() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["agents"], queryFn: agentService.list });
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["agents"] });
  return {
    ...query,
    createAgent: useMutation({ mutationFn: agentService.create, onSuccess: invalidate }),
    updateAgent: useMutation({ mutationFn: ({ id, payload }) => agentService.update(id, payload), onSuccess: invalidate }),
    suspendAgent: useMutation({ mutationFn: agentService.suspend, onSuccess: invalidate }),
    activateAgent: useMutation({ mutationFn: agentService.activate, onSuccess: invalidate }),
    blockAgent: useMutation({ mutationFn: agentService.block, onSuccess: invalidate }),
    deleteAgent: useMutation({ mutationFn: agentService.remove, onSuccess: invalidate })
  };
}
