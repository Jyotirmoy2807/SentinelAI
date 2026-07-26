from app.models.agent import Agent
from app.repositories.agent_repository import AgentRepository
from app.utils.time import utc_now


class AgentService:
    DEPARTMENTS = {"Finance", "HR", "Sales", "Operations", "IT"}
    STATUSES = {"ACTIVE", "SUSPENDED", "BLOCKED", "DELETED"}
    RISK_TIERS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    def __init__(self, repository: AgentRepository, enterprise_repository=None, budget_repository=None, governance_policy_repository=None):
        self.repository = repository
        self.enterprise_repository = enterprise_repository
        self.budget_repository = budget_repository
        self.governance_policy_repository = governance_policy_repository

    def list_agents(self) -> list[Agent]:
        return self.repository.list()

    def get_agent(self, agent_id: int) -> Agent | None:
        return self.repository.get(agent_id)

    def get_by_passport(self, passport_id: str) -> Agent | None:
        return self.repository.get_by_passport(passport_id)

    def register_agent(self, data: dict) -> Agent:
        self._validate(data)
        agent = self.repository.create(data)
        self.repository.db.commit()
        return agent

    def update_agent(self, agent: Agent, data: dict) -> Agent:
        self._validate({**self._to_dict(agent), **data})
        updated = self.repository.update(agent, data)
        self.repository.db.commit()
        return updated

    def set_status(self, agent: Agent, status: str) -> Agent:
        updated = self.repository.update(agent, {"status": status, "last_activity": utc_now()})
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
        agent.last_activity = utc_now()
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

    def _validate(self, data: dict) -> None:
        if data.get("department") not in self.DEPARTMENTS:
            raise ValueError(f"Unsupported department: {data.get('department')}")
        if data.get("status") not in self.STATUSES:
            raise ValueError(f"Unsupported agent status: {data.get('status')}")
        if data.get("risk_tier") not in self.RISK_TIERS:
            raise ValueError(f"Unsupported risk tier: {data.get('risk_tier')}")
        if self.budget_repository and not self.budget_repository.get_by_name(data.get("budget_profile", "")):
            raise ValueError(f"Unknown budget profile: {data.get('budget_profile')}")
        if self.enterprise_repository:
            enterprise_apis = self.enterprise_repository.list_active()
            operations_by_service: dict[str, set[str]] = {}
            for api in enterprise_apis:
                operations_by_service.setdefault(api.service_name, set()).add(api.operation)
            unknown_apis = sorted(set(data.get("allowed_apis", [])) - set(operations_by_service))
            if unknown_apis:
                raise ValueError(f"Unknown enterprise APIs: {', '.join(unknown_apis)}")
            valid_operations = set()
            for api_name in data.get("allowed_apis", []):
                valid_operations.update(operations_by_service.get(api_name, set()))
            unknown_operations = sorted(set(data.get("allowed_operations", [])) - valid_operations)
            if unknown_operations:
                raise ValueError(f"Unsupported operations for selected APIs: {', '.join(unknown_operations)}")
        if self.governance_policy_repository:
            policy_ids = {policy.policy_id for policy in self.governance_policy_repository.list_ordered()}
            unknown_groups = sorted(set(data.get("policy_groups", [])) - policy_ids)
            if unknown_groups:
                raise ValueError(f"Unknown governance policies: {', '.join(unknown_groups)}")

    def _to_dict(self, agent: Agent) -> dict:
        return {
            "passport_id": agent.passport_id,
            "name": agent.name,
            "owner": agent.owner,
            "department": agent.department,
            "version": agent.version,
            "status": agent.status,
            "trust_score": agent.trust_score,
            "risk_tier": agent.risk_tier,
            "allowed_apis": agent.allowed_apis,
            "allowed_operations": agent.allowed_operations,
            "budget_profile": agent.budget_profile,
            "policy_groups": agent.policy_groups,
            "reputation": agent.reputation,
        }
