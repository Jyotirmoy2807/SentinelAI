from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.policy import PolicyCreate, PolicyRead, PolicyUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("", response_model=list[PolicyRead])
def list_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_policies()


@router.post("", response_model=PolicyRead, status_code=status.HTTP_201_CREATED)
def create_policy(payload: PolicyCreate, services: ServiceContainer = Depends(get_services)):
    return services.policies.create_policy(payload.model_dump())


@router.get("/{policy_id}", response_model=PolicyRead)
def get_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    policy = services.policies.get_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.put("/{policy_id}", response_model=PolicyRead)
def update_policy(policy_id: int, payload: PolicyUpdate, services: ServiceContainer = Depends(get_services)):
    policy = services.policies.get_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return services.policies.update_policy(policy, payload.model_dump(exclude_unset=True))


@router.delete("/{policy_id}", response_model=PolicyRead)
def delete_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    policy = services.policies.get_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return services.policies.delete_policy(policy)
