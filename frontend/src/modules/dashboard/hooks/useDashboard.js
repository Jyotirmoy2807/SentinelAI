import { useQuery } from "@tanstack/react-query";
import { dashboardService } from "../services/dashboardService.js";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: dashboardService.summary,
    refetchInterval: 15000
  });
}
