# SentinelAI Implementation Notes

This prototype follows the architecture documents in `context/` as the source of truth.

## Backend Boundaries

- FastAPI routes only validate and return API payloads.
- LangGraph owns orchestration and conditional routing.
- Graph nodes are thin service callers and live-event emitters.
- Services own business logic.
- Repositories perform CRUD only.
- Enterprise adapters are invoked only by `ExecutionService`, which is called from the Enterprise Execution node.
- Audit and explainability are produced for every graph outcome.

## Governance Graph

Implemented nodes:

1. API Ingestion
2. Request Normalization
3. Agent Identity
4. Policy Engine
5. AI Firewall
6. Risk Engine
7. Budget Engine
8. Compliance Engine
9. Human Approval
10. Audit Engine
11. Enterprise Execution
12. Explainability
13. Response Builder

Human approval stores a pending approval and state snapshot. Approval actions resume from the Human Approval node using the stored state.

## Frontend Boundaries

- Pages compose feature and shared components.
- Hooks own React Query interactions.
- Services own Axios calls.
- Zustand stores UI-only state.
- React Flow mirrors the backend governance graph.
- WebSockets power live execution visualization.
