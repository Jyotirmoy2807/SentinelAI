from fastapi import APIRouter, Depends

from app.core.dependencies import get_services
from app.schemas.audit import AuditDetail, AuditLogRead
from app.services.container import ServiceContainer


router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("", response_model=list[AuditLogRead])
def list_audit(services: ServiceContainer = Depends(get_services)):
    return services.audit.list_recent(200)


@router.get("/{request_id}", response_model=AuditDetail)
def audit_detail(request_id: str, services: ServiceContainer = Depends(get_services)):
    execution_logs = services.execution.list_by_request(request_id)
    return services.audit.detail(request_id, execution_logs)
