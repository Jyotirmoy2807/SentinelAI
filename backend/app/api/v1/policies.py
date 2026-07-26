from fastapi import APIRouter, Depends

from app.core.dependencies import get_services
from app.schemas.policy import OpaPolicyRead
from app.services.container import ServiceContainer


router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("", response_model=list[OpaPolicyRead])
def list_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_policies()
