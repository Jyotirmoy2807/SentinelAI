export const governanceNodes = [
  { id: "api_ingestion", label: "API Ingestion", position: { x: 0, y: 165 } },
  { id: "request_normalization", label: "Request Normalization", position: { x: 205, y: 165 } },
  { id: "agent_identity", label: "Agent Identity", position: { x: 410, y: 165 } },
  { id: "risk_engine", label: "Risk Engine (NIST RMF)", position: { x: 615, y: 165 } },
  { id: "policy_engine", label: "OPA Policy Engine", position: { x: 820, y: 165 } },
  { id: "human_approval", label: "Human Approval", position: { x: 820, y: 20 } },
  { id: "enterprise_execution", label: "Enterprise Execution", position: { x: 1025, y: 165 } },
  { id: "audit_engine", label: "Audit (Splunk)", position: { x: 1025, y: 310 } },
  { id: "explainability", label: "Explainability", position: { x: 615, y: 310 } },
  { id: "response_builder", label: "Response Builder", position: { x: 410, y: 310 } }
];

export const governanceEdges = [
  ["api_ingestion", "request_normalization"],
  ["request_normalization", "agent_identity"],
  ["agent_identity", "risk_engine"],
  ["risk_engine", "policy_engine"],
  ["policy_engine", "audit_engine", "deny"],
  ["policy_engine", "human_approval", "approval required"],
  ["policy_engine", "enterprise_execution", "allow"],
  ["human_approval", "audit_engine", "rejected"],
  ["human_approval", "enterprise_execution", "approved"],
  ["enterprise_execution", "audit_engine"],
  ["audit_engine", "explainability"],
  ["explainability", "response_builder"]
].map(([source, target, label]) => ({
  id: `${source}-${target}`,
  source,
  target,
  label,
  type: "smoothstep",
  animated: false,
  markerEnd: { type: "arrowclosed" }
}));
