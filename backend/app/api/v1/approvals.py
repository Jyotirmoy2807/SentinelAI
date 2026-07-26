from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_services
from app.graph.graph import GovernanceGraph
from app.schemas.approval import ApprovalAction, ApprovalRead
from app.schemas.governance import GovernanceResponse
from app.services.container import ServiceContainer


router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("", response_model=list[ApprovalRead])
def list_approvals(services: ServiceContainer = Depends(get_services)):
    return services.approvals.list_approvals()


@router.get("/pending", response_model=list[ApprovalRead])
def list_pending(services: ServiceContainer = Depends(get_services)):
    return services.approvals.list_pending()


@router.get("/{approval_id}", response_model=ApprovalRead)
def get_approval(approval_id: str, services: ServiceContainer = Depends(get_services)):
    approval = services.approvals.get_approval(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval


@router.post("/{approval_id}/approve", response_model=GovernanceResponse)
async def approve(approval_id: str, payload: ApprovalAction, services: ServiceContainer = Depends(get_services)):
    approval = services.approvals.get_approval(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    updated = services.approvals.approve(approval, payload.approver, payload.comments)
    graph = GovernanceGraph(services)
    result = await graph.resume(updated.state_snapshot, "APPROVED", payload.approver, payload.comments)
    return result["response"]


@router.post("/{approval_id}/reject", response_model=GovernanceResponse)
async def reject(approval_id: str, payload: ApprovalAction, services: ServiceContainer = Depends(get_services)):
    approval = services.approvals.get_approval(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    updated = services.approvals.reject(approval, payload.approver, payload.comments)
    graph = GovernanceGraph(services)
    result = await graph.resume(updated.state_snapshot, "REJECTED", payload.approver, payload.comments)
    return result["response"]
