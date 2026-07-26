import { useQuery } from "@tanstack/react-query";
import { auditService } from "../services/auditService.js";

export function useAudit(requestId) {
  const list = useQuery({ queryKey: ["audit"], queryFn: auditService.list, refetchInterval: 15000 });
  const detail = useQuery({
    queryKey: ["audit", requestId],
    queryFn: () => auditService.detail(requestId),
    enabled: Boolean(requestId)
  });
  return { list, detail };
}
