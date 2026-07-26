export const governanceNodes = [
  { id: "api_ingestion", label: "API Ingestion", position: { x: 0, y: 0 } },
  { id: "request_normalization", label: "Request Normalization", position: { x: 260, y: 0 } },
  { id: "agent_identity", label: "Agent Identity", position: { x: 520, y: 0 } },
  { id: "risk_engine", label: "Risk Engine (NIST RMF)", position: { x: 780, y: 0 } },
  { id: "policy_engine", label: "OPA Policy Engine", position: { x: 1040, y: 0 } },
  { id: "human_approval", label: "Human Approval", position: { x: 1300, y: -140 } },
  { id: "enterprise_execution", label: "Enterprise Execution", position: { x: 1560, y: 0 } },
  { id: "audit_engine", label: "Audit (Splunk)", position: { x: 1820, y: 0 } },
  { id: "explainability", label: "Explainability", position: { x: 2080, y: 0 } },
  { id: "response_builder", label: "Response Builder", position: { x: 2340, y: 0 } }
];

export const governanceEdges = [
  ["api_ingestion", "request_normalization"],
  ["request_normalization", "agent_identity"],
  ["agent_identity", "risk_engine"],
  ["agent_identity", "audit_engine"],
  ["risk_engine", "policy_engine"],
  ["policy_engine", "audit_engine"],
  ["policy_engine", "human_approval"],
  ["policy_engine", "enterprise_execution"],
  ["human_approval", "audit_engine"],
  ["human_approval", "enterprise_execution"],
  ["enterprise_execution", "audit_engine"],
  ["audit_engine", "explainability"],
  ["explainability", "response_builder"]
].map(([source, target]) => ({ id: `${source}-${target}`, source, target, animated: false }));
