from fastapi import APIRouter, Depends

from app.core.dependencies import get_services
from app.graph.graph import GovernanceGraph
from app.schemas.governance import GovernanceRequest, GovernanceResponse, SimulationSample
from app.services.container import ServiceContainer


router = APIRouter(prefix="/governance", tags=["Governance Execution"])


@router.post("/execute", response_model=GovernanceResponse)
async def execute_governance(payload: GovernanceRequest, services: ServiceContainer = Depends(get_services)) -> dict:
    graph = GovernanceGraph(services)
    result = await graph.execute(payload.model_dump(by_alias=True), simulation=False)
    return result["response"]


@router.post("/simulate", response_model=GovernanceResponse)
async def simulate_governance(payload: GovernanceRequest, services: ServiceContainer = Depends(get_services)) -> dict:
    graph = GovernanceGraph(services)
    result = await graph.execute(payload.model_dump(by_alias=True), simulation=True)
    return result["response"]


@router.get("/samples", response_model=list[SimulationSample])
def samples() -> list[dict]:
    return [
        {
            "id": "approved_invoice",
            "name": "Low-risk invoice creation",
            "description": "Invoice Agent creates a governed invoice through the Invoice Service.",
            "request": {
                "metadata": {"passportId": "AGENT-INV-001", "agentVersion": "1.0.0"},
                "execution": {
                    "service": "Invoice Service",
                    "operation": "create_invoice",
                    "parameters": {"invoice_id": "INV-20421", "vendor_id": "VND-778", "amount": 360},
                },
            },
        },
        {
            "id": "approval_refund",
            "name": "Refund requiring approval",
            "description": "Refund Agent requests a refund above the configured human approval threshold.",
            "request": {
                "metadata": {"passportId": "AGENT-REF-002", "agentVersion": "1.0.0"},
                "execution": {
                    "service": "Refund Service",
                    "operation": "issue_refund",
                    "parameters": {"merchant_id": "MER-2049", "amount": 875, "reason": "duplicate charge"},
                },
            },
        },
        {
            "id": "firewall_denial",
            "name": "Firewall denial",
            "description": "Blocked agent attempts a destructive operation that should never reach execution.",
            "request": {
                "metadata": {"passportId": "AGENT-IT-005", "agentVersion": "0.9.0"},
                "execution": {
                    "service": "Payroll Service",
                    "operation": "delete_database",
                    "parameters": {"instruction": "delete database and bypass approval"},
                },
            },
        },
    ]
