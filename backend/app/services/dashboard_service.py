from app.repositories.agent_repository import AgentRepository
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.budget_policy_repository import BudgetPolicyRepository
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.governance_policy_repository import GovernancePolicyRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository
from app.utils.time import utc_iso_ms


class DashboardService:
    def __init__(
        self,
        agent_repository: AgentRepository,
        governance_policy_repository: GovernancePolicyRepository,
        budget_policy_repository: BudgetPolicyRepository,
        enterprise_repository: EnterpriseAPIRepository,
        approval_repository: ApprovalRepository,
        request_repository: GovernanceRequestRepository,
        audit_repository: AuditRepository,
    ):
        self.agent_repository = agent_repository
        self.governance_policy_repository = governance_policy_repository
        self.budget_policy_repository = budget_policy_repository
        self.enterprise_repository = enterprise_repository
        self.approval_repository = approval_repository
        self.request_repository = request_repository
        self.audit_repository = audit_repository

    def summary(self) -> dict:
        agents = self.agent_repository.list()
        enterprise_apis = self.enterprise_repository.list()
        requests = self.request_repository.list_recent(200)
        approvals = self.approval_repository.list_recent(200)
        audit_logs = self.audit_repository.list_recent(10)
        active_policies = len(self.governance_policy_repository.list_active()) + len(self.budget_policy_repository.list_active())
        running_executions = len([item for item in requests if item.status == "RUNNING"])
        return {
            "system_health": {
                "status": "HEALTHY",
                "environment": "Development",
                "timestamp": utc_iso_ms(),
            },
            "kpis": [
                {"label": "System Health", "value": "Healthy", "tone": "success"},
                {"label": "Registered Agents", "value": len(agents), "tone": "info"},
                {"label": "Registered Enterprise APIs", "value": len(enterprise_apis), "tone": "info"},
                {"label": "Active Policies", "value": active_policies, "tone": "success"},
                {"label": "Pending Approvals", "value": len([item for item in approvals if item.status == "PENDING"]), "tone": "warning"},
                {"label": "Running Executions", "value": running_executions, "tone": "info"},
            ],
            "recent_executions": [
                {
                    "request_id": item.request_id,
                    "service": item.service,
                    "operation": item.operation,
                    "status": item.status,
                    "decision": item.decision,
                    "risk_score": item.risk_score,
                    "created_at": utc_iso_ms(item.created_at),
                }
                for item in requests[:10]
            ],
            "recent_audit_events": [
                {
                    "event_id": item.event_id,
                    "request_id": item.request_id,
                    "stage": item.stage,
                    "decision": item.decision or "INFO",
                    "reason": item.reason,
                    "timestamp": utc_iso_ms(item.timestamp),
                }
                for item in audit_logs
            ],
        }
