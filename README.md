# SentinelAI

SentinelAI is a prototype Enterprise AI Governance Platform. It demonstrates the documented governance workflow from Agent Passport identity through policy, firewall, risk, budget, compliance, human approval, audit, enterprise execution, explainability, and standardized response building.

## Project Structure

```text
backend/
  app/
    api/            FastAPI REST and WebSocket surface
    graph/          LangGraph orchestration and routing
    graph/nodes/    One governance node per file
    services/       Business logic and governance decisions
    repositories/   CRUD-only persistence layer
    models/         SQLAlchemy entities
    schemas/        Pydantic DTOs
    adapters/       Mock enterprise adapter layer
    database/       SQLite setup and seed data
frontend/
  src/
    layouts/
    components/
    modules/        Dashboard, agents, governance, enterprise, execution, approvals, audit, settings, simulation
context/            Architecture source-of-truth documents
docs/               Implementation notes
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

The backend seeds SQLite automatically on startup with agents, policies, enterprise APIs, firewall rules, budgets, compliance rules, approvals, governance requests, and audit logs.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Set `VITE_API_BASE_URL` if the backend is not running at `http://localhost:8000/api/v1`.

## Demo Passports

Use these seeded Agent Passports in the live execution page or API requests:

- `AGENT-INV-001` - Invoice Agent
- `AGENT-REF-002` - Refund Agent
- `AGENT-MER-003` - Merchant Agent
- `AGENT-BOOK-004` - Suspended Booking Agent
- `AGENT-IT-005` - Blocked IT Support Agent

## Key Endpoints

- `GET /api/v1/health`
- `GET /api/v1/dashboard`
- `POST /api/v1/governance/execute`
- `POST /api/v1/governance/simulate`
- `GET /api/v1/governance/samples`
- `WS /api/v1/ws/governance/live`
- `GET /api/v1/approvals`
- `POST /api/v1/approvals/{approval_id}/approve`
- `GET /api/v1/audit`

## Verification

Backend syntax and graph execution were verified with the local virtual environment. Frontend production build was verified with Vite.
