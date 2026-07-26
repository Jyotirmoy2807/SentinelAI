from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.compliance import ComplianceRuleCreate, ComplianceRuleRead, ComplianceRuleUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("", response_model=list[ComplianceRuleRead])
def list_rules(services: ServiceContainer = Depends(get_services)):
    return services.compliance.list_rules()


@router.post("", response_model=ComplianceRuleRead, status_code=status.HTTP_201_CREATED)
def create_rule(payload: ComplianceRuleCreate, services: ServiceContainer = Depends(get_services)):
    return services.compliance.create_rule(payload.model_dump())


@router.put("/{rule_id}", response_model=ComplianceRuleRead)
def update_rule(rule_id: int, payload: ComplianceRuleUpdate, services: ServiceContainer = Depends(get_services)):
    rule = services.compliance.get_rule(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Compliance rule not found")
    return services.compliance.update_rule(rule, payload.model_dump(exclude_unset=True))


@router.delete("/{rule_id}", response_model=ComplianceRuleRead)
def delete_rule(rule_id: int, services: ServiceContainer = Depends(get_services)):
    rule = services.compliance.get_rule(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Compliance rule not found")
    return services.compliance.delete_rule(rule)
