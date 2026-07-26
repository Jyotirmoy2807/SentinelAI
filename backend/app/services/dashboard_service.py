from collections import Counter
from datetime import datetime, timedelta

from app.repositories.agent_repository import AgentRepository
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository


class DashboardService:
    def __init__(
        self,
        agent_repository: AgentRepository,
        policy_catalog,
        enterprise_repository: EnterpriseAPIRepository,
        approval_repository: ApprovalRepository,
        request_repository: GovernanceRequestRepository,
        audit_repository: AuditRepository,
    ):
        self.agent_repository = agent_repository
        self.policy_catalog = policy_catalog
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
        today = datetime.utcnow().date()
        requests_today = [item for item in requests if item.created_at.date() == today]
        denied = [item for item in requests if item.decision == "DENY"]
        avg_risk = round(sum(item.risk_score for item in requests) / max(len(requests), 1), 1)
        avg_duration = round(sum(item.duration_ms for item in requests) / max(len(requests), 1), 1)
        return {
            "kpis": [
                {"label": "Registered Agents", "value": len(agents), "change": "+4 seeded", "tone": "info"},
                {"label": "Active Agents", "value": len([item for item in agents if item.status == "ACTIVE"]), "tone": "success"},
                {"label": "Blocked Agents", "value": len([item for item in agents if item.status == "BLOCKED"]), "tone": "danger"},
                {"label": "Enterprise APIs", "value": len(enterprise_apis), "tone": "info"},
                {"label": "OPA Policies", "value": self.policy_catalog.count_active(), "tone": "success"},
                {"label": "Pending Approvals", "value": len([item for item in approvals if item.status == "PENDING"]), "tone": "warning"},
                {"label": "Requests Today", "value": len(requests_today), "tone": "info"},
                {"label": "Denied Requests", "value": len(denied), "tone": "danger"},
                {"label": "Average Risk", "value": avg_risk, "tone": "warning"},
                {"label": "Avg Execution Time", "value": f"{avg_duration} ms", "tone": "info"},
            ],
            "request_trend": self._request_trend(requests),
            "risk_distribution": self._risk_distribution(requests),
            "approval_trend": self._approval_trend(approvals),
            "recent_activity": [
                {
                    "timestamp": item.timestamp.isoformat(),
                    "title": item.stage.replace("_", " ").title(),
                    "description": item.reason,
                    "status": item.decision or "INFO",
                }
                for item in audit_logs
            ],
        }

    def _request_trend(self, requests: list) -> list[dict]:
        rows = []
        for offset in range(6, -1, -1):
            date = datetime.utcnow().date() - timedelta(days=offset)
            count = len([item for item in requests if item.created_at.date() == date])
            rows.append({"date": date.strftime("%b %d"), "requests": count})
        return rows

    def _risk_distribution(self, requests: list) -> list[dict]:
        buckets = {"Low": 0, "Medium": 0, "High": 0}
        for item in requests:
            if item.risk_score >= 70:
                buckets["High"] += 1
            elif item.risk_score >= 40:
                buckets["Medium"] += 1
            else:
                buckets["Low"] += 1
        if not requests:
            buckets = {"Low": 9, "Medium": 4, "High": 2}
        return [{"name": key, "value": value} for key, value in buckets.items()]

    def _approval_trend(self, approvals: list) -> list[dict]:
        counts = Counter(item.status.title() for item in approvals)
        if not approvals:
            counts.update({"Pending": 3, "Approved": 8, "Rejected": 2})
        return [{"name": key, "value": value} for key, value in counts.items()]
