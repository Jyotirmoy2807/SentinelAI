from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.agent import AgentCreate, AgentRead, AgentUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=list[AgentRead])
def list_agents(services: ServiceContainer = Depends(get_services)):
    return services.agents.list_agents()


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(payload: AgentCreate, services: ServiceContainer = Depends(get_services)):
    try:
        return services.agents.register_agent(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, services: ServiceContainer = Depends(get_services)):
    agent = services.agents.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentRead)
def update_agent(agent_id: int, payload: AgentUpdate, services: ServiceContainer = Depends(get_services)):
    agent = services.agents.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    try:
        return services.agents.update_agent(agent, payload.model_dump(exclude_unset=True))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{agent_id}/suspend", response_model=AgentRead)
def suspend_agent(agent_id: int, services: ServiceContainer = Depends(get_services)):
    return _set_agent_status(agent_id, "SUSPENDED", services)


@router.post("/{agent_id}/activate", response_model=AgentRead)
def activate_agent(agent_id: int, services: ServiceContainer = Depends(get_services)):
    return _set_agent_status(agent_id, "ACTIVE", services)


@router.post("/{agent_id}/block", response_model=AgentRead)
def block_agent(agent_id: int, services: ServiceContainer = Depends(get_services)):
    return _set_agent_status(agent_id, "BLOCKED", services)


@router.delete("/{agent_id}", response_model=AgentRead)
def delete_agent(agent_id: int, services: ServiceContainer = Depends(get_services)):
    agent = services.agents.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return services.agents.delete_agent(agent)


def _set_agent_status(agent_id: int, status_value: str, services: ServiceContainer):
    agent = services.agents.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return services.agents.set_status(agent, status_value)
