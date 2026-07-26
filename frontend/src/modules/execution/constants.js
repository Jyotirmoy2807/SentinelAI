export const governanceNodes = [
  { id: "api_ingestion", label: "API Ingestion", position: { x: 0, y: 0 } },
  { id: "request_normalization", label: "Request Normalization", position: { x: 260, y: 0 } },
  { id: "agent_identity", label: "Agent Identity", position: { x: 520, y: 0 } },
  { id: "policy_engine", label: "Policy Engine", position: { x: 780, y: 0 } },
  { id: "ai_firewall", label: "AI Firewall", position: { x: 1040, y: 0 } },
  { id: "risk_engine", label: "Risk Engine", position: { x: 1300, y: 0 } },
  { id: "budget_engine", label: "Budget Engine", position: { x: 1560, y: 0 } },
  { id: "compliance_engine", label: "Compliance Engine", position: { x: 1820, y: 0 } },
  { id: "human_approval", label: "Human Approval", position: { x: 2080, y: -140 } },
  { id: "audit_engine", label: "Audit Engine", position: { x: 2340, y: 0 } },
  { id: "enterprise_execution", label: "Enterprise Execution", position: { x: 2600, y: 0 } },
  { id: "explainability", label: "Explainability", position: { x: 2860, y: 0 } },
  { id: "response_builder", label: "Response Builder", position: { x: 3120, y: 0 } }
];

export const governanceEdges = [
  ["api_ingestion", "request_normalization"],
  ["request_normalization", "agent_identity"],
  ["agent_identity", "policy_engine"],
  ["agent_identity", "audit_engine"],
  ["policy_engine", "ai_firewall"],
  ["policy_engine", "audit_engine"],
  ["ai_firewall", "risk_engine"],
  ["ai_firewall", "audit_engine"],
  ["risk_engine", "budget_engine"],
  ["budget_engine", "compliance_engine"],
  ["budget_engine", "audit_engine"],
  ["compliance_engine", "human_approval"],
  ["compliance_engine", "audit_engine"],
  ["human_approval", "audit_engine"],
  ["audit_engine", "enterprise_execution"],
  ["audit_engine", "explainability"],
  ["enterprise_execution", "explainability"],
  ["explainability", "response_builder"]
].map(([source, target]) => ({ id: `${source}-${target}`, source, target, animated: false }));
