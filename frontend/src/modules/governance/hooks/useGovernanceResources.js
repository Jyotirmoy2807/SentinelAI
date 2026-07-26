import { useQueries } from "@tanstack/react-query";
import { governanceService } from "../services/governanceService.js";

export function useGovernanceResources() {
  const [policies, settings] = useQueries({
    queries: ["policies", "settings"].map((kind) => ({
      queryKey: [kind],
      queryFn: () => (kind === "settings" ? governanceService.settings() : governanceService.list(kind))
    }))
  });
  return {
    policies,
    settings
  };
}
