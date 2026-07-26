export const governanceNodes = [
  { id: "api_ingestion", label: "API Ingestion", position: { x: 0, y: 60 } },
  { id: "request_normalization", label: "Request Normalization", position: { x: 180, y: 60 } },
  { id: "agent_identity", label: "Agent Identity", position: { x: 360, y: 60 } },
  { id: "risk_engine", label: "Risk Engine (NIST RMF)", position: { x: 540, y: 60 } },
  { id: "policy_engine", label: "OPA Policy Engine", position: { x: 720, y: 60 } },
  { id: "human_approval", label: "Human Approval", position: { x: 540, y: 195 } },
  { id: "enterprise_execution", label: "Enterprise Execution", position: { x: 720, y: 195 } },
  { id: "audit_engine", label: "Audit (Splunk)", position: { x: 900, y: 195 } },
  { id: "explainability", label: "Explainability", position: { x: 720, y: 330 } },
  { id: "response_builder", label: "Response Builder", position: { x: 900, y: 330 } }
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
