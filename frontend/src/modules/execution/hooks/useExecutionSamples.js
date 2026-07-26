import { useQuery } from "@tanstack/react-query";
import { executionService } from "../services/executionService.js";

export function useExecutionSamples() {
  return useQuery({ queryKey: ["execution", "samples"], queryFn: executionService.samples });
}
