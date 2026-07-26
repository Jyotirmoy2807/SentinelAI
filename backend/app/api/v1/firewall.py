from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.firewall import FirewallRuleCreate, FirewallRuleRead, FirewallRuleUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/firewall", tags=["Firewall"])


@router.get("", response_model=list[FirewallRuleRead])
def list_rules(services: ServiceContainer = Depends(get_services)):
    return services.firewall.list_rules()


@router.post("", response_model=FirewallRuleRead, status_code=status.HTTP_201_CREATED)
def create_rule(payload: FirewallRuleCreate, services: ServiceContainer = Depends(get_services)):
    return services.firewall.create_rule(payload.model_dump())


@router.put("/{rule_id}", response_model=FirewallRuleRead)
def update_rule(rule_id: int, payload: FirewallRuleUpdate, services: ServiceContainer = Depends(get_services)):
    rule = services.firewall.get_rule(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Firewall rule not found")
    return services.firewall.update_rule(rule, payload.model_dump(exclude_unset=True))


@router.delete("/{rule_id}", response_model=FirewallRuleRead)
def delete_rule(rule_id: int, services: ServiceContainer = Depends(get_services)):
    rule = services.firewall.get_rule(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Firewall rule not found")
    return services.firewall.delete_rule(rule)
