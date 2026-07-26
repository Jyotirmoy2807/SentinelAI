from datetime import datetime

from app.models.agent import Agent
from app.repositories.agent_repository import AgentRepository


class AgentService:
    def __init__(self, repository: AgentRepository):
        self.repository = repository

    def list_agents(self) -> list[Agent]:
        return self.repository.list()

    def get_agent(self, agent_id: int) -> Agent | None:
        return self.repository.get(agent_id)

    def get_by_passport(self, passport_id: str) -> Agent | None:
        return self.repository.get_by_passport(passport_id)

    def register_agent(self, data: dict) -> Agent:
        agent = self.repository.create(data)
        self.repository.db.commit()
        return agent

    def update_agent(self, agent: Agent, data: dict) -> Agent:
        updated = self.repository.update(agent, data)
        self.repository.db.commit()
        return updated

    def set_status(self, agent: Agent, status: str) -> Agent:
        updated = self.repository.update(agent, {"status": status, "last_activity": datetime.utcnow()})
        self.repository.db.commit()
        return updated

    def delete_agent(self, agent: Agent) -> Agent:
        updated = self.repository.update(agent, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def load_passport(self, passport_id: str) -> dict:
        agent = self.repository.get_by_passport(passport_id)
        if agent is None:
            return {
                "passport_id": passport_id,
                "status": "UNKNOWN",
                "decision": "DENY",
                "reason": "Agent Passport was not found.",
            }
        if agent.status != "ACTIVE":
            return {
                "passport_id": agent.passport_id,
                "agent_name": agent.name,
                "department": agent.department,
                "owner": agent.owner,
                "status": agent.status,
                "decision": "DENY",
                "reason": f"Agent status is {agent.status}. Only ACTIVE agents can execute enterprise actions.",
            }
        agent.last_activity = datetime.utcnow()
        self.repository.db.flush()
        return {
            "passport_id": agent.passport_id,
            "agent_name": agent.name,
            "owner": agent.owner,
            "department": agent.department,
            "version": agent.version,
            "status": agent.status,
            "trust_score": agent.trust_score,
            "reputation": agent.reputation,
            "risk_tier": agent.risk_tier,
            "allowed_apis": agent.allowed_apis or [],
            "allowed_operations": agent.allowed_operations or [],
            "policy_groups": agent.policy_groups or [],
            "budget_profile": agent.budget_profile,
            "decision": "ALLOW",
            "reason": "Agent Passport verified.",
        }
