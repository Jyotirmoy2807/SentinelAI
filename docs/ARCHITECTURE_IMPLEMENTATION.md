# SentinelAI v2 Implementation Notes

This refactor removes the old standalone AI Firewall, Budget Engine, and Compliance Engine. Their decision responsibilities now live in OPA Rego policy.

## Backend Boundaries

- FastAPI routes only validate and return API payloads.
- LangGraph owns orchestration and conditional routing.
- Graph nodes are thin service callers and live-event emitters.
- NIST RMF risk logic lives in `RiskService`.
- Governance Policies and Budget Policies are stored as JSON records and compiled into one `governance.rego` bundle.
- Policy decisions are delegated to OPA through `OpaPolicyAdapter`.
- Splunk-compatible audit events are emitted through an abstract audit sink.
- Explainability reads audit events and does not maintain a separate execution history.
- `ExecutionService` invokes the configuration-driven `UniversalAPIAdapter` only after governance allow or approval.

## Universal API Adapter

The Enterprise API Registry stores one endpoint configuration per `(service, operation)`, including method, base URL, path, authentication type/config, timeout, retry count, version, status, required policies, and endpoint metadata. The Universal API Adapter resolves that registry entry, injects configured authentication, sends the original `execution.parameters` payload, and captures the upstream response. Governance-denied requests route directly to audit and response and never invoke enterprise execution.

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

## Policy Management

JSON policy records are the source of truth.

- Governance Policies support create, edit, delete, duplicate, enable, and disable.
- Budget Policies have separate CRUD and contain only name, department, daily/monthly/transaction limits, approval threshold, spend totals, and status.
- Deployment generates a single `governance.rego`, runs `opa fmt`, runs `opa check`, records deployment status, and relies on OPA watch mode for reload.
- Policy versions capture snapshots for history, compare, and restore.

## OPA Policy Scope

Generated Rego covers:

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
