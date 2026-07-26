# SentinelAI v2

SentinelAI is a prototype Enterprise AI Governance Platform. Version 2 simplifies the governance layer around three enterprise-grade primitives:

- Open Policy Agent (OPA) for policy decisions
- NIST Risk Management Framework (RMF) alignment for risk assessment
- Splunk-compatible structured JSON audit events for observability

## Governance Pipeline

```text
START
API Ingestion
Request Normalization
Agent Identity
Risk Engine (NIST RMF)
OPA Policy Engine
  Deny -> Audit -> Explainability -> Response
  Approval Required -> Human Approval -> Audit -> Explainability -> Response
  Allow -> Enterprise Execution -> Audit -> Explainability -> Response
END
```

## Project Structure

```text
backend/
  app/
    api/             FastAPI REST and WebSocket surface
    graph/           LangGraph orchestration and routing
    graph/nodes/     One governance node per stage
    services/        Risk, OPA policy, audit, approval, execution, explainability
    repositories/    CRUD-only persistence layer
    models/          SQLAlchemy entities
    schemas/         Pydantic DTOs
    adapters/        OPA, Splunk-compatible audit sink, Universal API Adapter
    policies/rego/   OPA Rego policy files
    database/        SQLite setup and seed data
frontend/
  src/
    modules/         Dashboard, agents, governance, enterprise, approvals, audit, settings, simulation
context/             Original architecture documents
docs/                Implementation notes
```

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## OPA

SentinelAI sends policy decisions to OPA REST at:

```text
http://localhost:8181/v1/data/sentinelai/governance/decision
```

Run OPA with the bundled Rego policy:

```bash
opa run --server --watch app/policies/rego
```

If OPA is unavailable, SentinelAI fails closed with a `DENY` decision.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

The console redirects `/` to `/dashboard` and provides a dedicated 404 page for unknown routes.

Set `VITE_API_BASE_URL` if the backend is not running at `http://localhost:8000/api/v1`.

## Demo Passports

- `AGENT-INV-001` - Invoice Agent
- `AGENT-REF-002` - Refund Agent
- `AGENT-MER-003` - Merchant Agent
- `AGENT-BOOK-004` - Suspended Booking Agent
- `AGENT-IT-005` - Blocked IT Support Agent

## Key Endpoints

- `GET /api/v1/health`
- `GET /api/v1/dashboard`
- `GET /api/v1/policies`
- `GET /api/v1/policies/governance`
- `POST /api/v1/policies/governance`
- `GET /api/v1/policies/budgets`
- `POST /api/v1/policies/budgets`
- `POST /api/v1/policies/deploy`
- `GET /api/v1/policies/history`
- `POST /api/v1/governance/execute`
- `POST /api/v1/governance/simulate`
- `GET /api/v1/governance/samples`
- `WS /api/v1/ws/governance/live`
- `GET /api/v1/enterprise`
- `GET /api/v1/enterprise/lookups`
- `GET /api/v1/approvals`
- `POST /api/v1/approvals/{approval_id}/approve`
- `GET /api/v1/audit`

The app includes a prototype migration that rebuilds the old v1 `audit_logs` table into the v2 Splunk-compatible schema on startup.

Initial seed data is limited to Agent Passports, Enterprise APIs, Governance Policies, and Budget Policies. Runtime tables such as audit logs, approvals, execution history, and workflow history are populated dynamically during execution.
