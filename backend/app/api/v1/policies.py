from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.policy import OpaPolicyCreate, OpaPolicyRead
from app.services.container import ServiceContainer


router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("", response_model=list[OpaPolicyRead])
def list_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_policies()


@router.post("", response_model=OpaPolicyRead, status_code=status.HTTP_201_CREATED)
def create_policy(payload: OpaPolicyCreate, services: ServiceContainer = Depends(get_services)):
    try:
        return services.policies.create_policy(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
