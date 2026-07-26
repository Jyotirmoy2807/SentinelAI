from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import get_services
from app.schemas.policy import (
    BudgetPolicyCreate,
    BudgetPolicyRead,
    BudgetPolicyUpdate,
    GovernancePolicyCreate,
    GovernancePolicyRead,
    GovernancePolicyUpdate,
    PolicyCompareRead,
    PolicyDeploymentRead,
    PolicyLookupRead,
    PolicyVersionRead,
)
from app.services.container import ServiceContainer


router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("", response_model=list[GovernancePolicyRead])
def list_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_governance_policies()


@router.get("/lookups", response_model=PolicyLookupRead)
def policy_lookups(services: ServiceContainer = Depends(get_services)):
    return services.policies.lookups()


@router.get("/governance", response_model=list[GovernancePolicyRead])
def list_governance_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_governance_policies()


@router.post("/governance", response_model=GovernancePolicyRead, status_code=status.HTTP_201_CREATED)
def create_governance_policy(payload: GovernancePolicyCreate, services: ServiceContainer = Depends(get_services)):
    try:
        return services.policies.create_governance_policy(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/governance/{policy_id}", response_model=GovernancePolicyRead)
def update_governance_policy(policy_id: int, payload: GovernancePolicyUpdate, services: ServiceContainer = Depends(get_services)):
    policy = _get_governance(policy_id, services)
    try:
        return services.policies.update_governance_policy(policy, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/governance/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_governance_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    services.policies.delete_governance_policy(_get_governance(policy_id, services))


@router.post("/governance/{policy_id}/duplicate", response_model=GovernancePolicyRead)
def duplicate_governance_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.duplicate_governance_policy(_get_governance(policy_id, services))


@router.post("/governance/{policy_id}/enable", response_model=GovernancePolicyRead)
def enable_governance_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.set_governance_enabled(_get_governance(policy_id, services), True)


@router.post("/governance/{policy_id}/disable", response_model=GovernancePolicyRead)
def disable_governance_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.set_governance_enabled(_get_governance(policy_id, services), False)


@router.get("/budgets", response_model=list[BudgetPolicyRead])
def list_budget_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.list_budget_policies()


@router.post("/budgets", response_model=BudgetPolicyRead, status_code=status.HTTP_201_CREATED)
def create_budget_policy(payload: BudgetPolicyCreate, services: ServiceContainer = Depends(get_services)):
    try:
        return services.policies.create_budget_policy(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/budgets/{policy_id}", response_model=BudgetPolicyRead)
def update_budget_policy(policy_id: int, payload: BudgetPolicyUpdate, services: ServiceContainer = Depends(get_services)):
    policy = _get_budget(policy_id, services)
    try:
        return services.policies.update_budget_policy(policy, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/budgets/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    services.policies.delete_budget_policy(_get_budget(policy_id, services))


@router.post("/budgets/{policy_id}/duplicate", response_model=BudgetPolicyRead)
def duplicate_budget_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.duplicate_budget_policy(_get_budget(policy_id, services))


@router.post("/budgets/{policy_id}/activate", response_model=BudgetPolicyRead)
def activate_budget_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.set_budget_status(_get_budget(policy_id, services), "ACTIVE")


@router.post("/budgets/{policy_id}/deactivate", response_model=BudgetPolicyRead)
def deactivate_budget_policy(policy_id: int, services: ServiceContainer = Depends(get_services)):
    return services.policies.set_budget_status(_get_budget(policy_id, services), "INACTIVE")


@router.post("/deploy", response_model=PolicyDeploymentRead)
def deploy_policies(services: ServiceContainer = Depends(get_services)):
    return services.policies.deploy()


@router.get("/deployments/latest", response_model=PolicyDeploymentRead | None)
def latest_deployment(services: ServiceContainer = Depends(get_services)):
    return services.policies.latest_deployment()


@router.get("/history", response_model=list[PolicyVersionRead])
def policy_history(services: ServiceContainer = Depends(get_services)):
    return services.policies.history()


@router.get("/history/compare", response_model=PolicyCompareRead)
def compare_versions(left: str = Query(...), right: str = Query(...), services: ServiceContainer = Depends(get_services)):
    try:
        return services.policies.compare_versions(left, right)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/history/{version_id}/restore", response_model=PolicyDeploymentRead)
def restore_version(version_id: str, services: ServiceContainer = Depends(get_services)):
    try:
        return services.policies.restore_version(version_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def _get_governance(policy_id: int, services: ServiceContainer):
    policy = services.policies.get_governance_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Governance policy not found")
    return policy


def _get_budget(policy_id: int, services: ServiceContainer):
    policy = services.policies.get_budget_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Budget policy not found")
    return policy
