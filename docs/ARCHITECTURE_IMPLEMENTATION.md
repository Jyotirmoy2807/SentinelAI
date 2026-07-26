# SentinelAI v2 Implementation Notes

This refactor removes the old standalone AI Firewall, Budget Engine, and Compliance Engine. Their decision responsibilities now live in OPA Rego policy.

## Backend Boundaries

- FastAPI routes only validate and return API payloads.
- LangGraph owns orchestration and conditional routing.
- Graph nodes are thin service callers and live-event emitters.
- NIST RMF risk logic lives in `RiskService`.
- Policy decisions are delegated to OPA through `OpaPolicyAdapter`.
- Splunk-compatible audit events are emitted through an abstract audit sink.
- Explainability reads audit events and does not maintain a separate execution history.
- Enterprise adapters are invoked only by `ExecutionService`, after governance allow or approval.

## Governance Graph

Implemented nodes:

1. API Ingestion
2. Request Normalization
3. Agent Identity
4. Risk Engine (NIST RMF)
5. OPA Policy Engine
6. Human Approval
7. Enterprise Execution
8. Audit (Splunk-compatible)
9. Explainability
10. Response Builder

## OPA Policy Scope

The bundled Rego policy covers:

- blocked APIs
- forbidden tools/actions
- destructive operation denial
- out-of-scope agent behavior
- transaction limits
- approval thresholds
- PCI-style payment review
- GDPR-style personal data restrictions
- risk-score authorization thresholds

## Audit Event Shape

Every persisted audit event is Splunk-compatible JSON with:

- `timestamp`
- `requestId`
- `agent`
- `action`
- `policy`
- `riskScore`
- `decision`
- `approvalStatus`
- `latency`
- `reason`
- `enterpriseAPI`

The current sink persists events to SQLite. Future Splunk HEC, OpenSearch, or ELK sinks can replace the sink adapter without changing governance business logic.
