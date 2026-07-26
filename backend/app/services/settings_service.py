from app.core.config import Settings


class SettingsService:
    def __init__(self, settings: Settings, services=None):
        self.settings = settings
        self.services = services

    def read(self) -> dict:
        return {
            "app_name": self.settings.app_name,
            "app_env": self.settings.app_env,
            "api_v1_prefix": self.settings.api_v1_prefix,
            "graph_version": self.settings.graph_version,
            "database_url": self.settings.database_url,
            "cors_origins": self.settings.cors_origins,
            "enterprise_executor": "UniversalAPIAdapter",
            "opa_url": self.settings.opa_url,
            "opa_decision_path": self.settings.opa_decision_path,
            "opa_policy_bundle_path": self.settings.opa_policy_bundle_path,
            "opa_cli_path": self.settings.opa_cli_path,
            "audit_sink": self.settings.audit_sink,
            "log_level": self.settings.log_level,
        }

    def lookups(self) -> dict:
        policies = self.services.policies.list_governance_policies() if self.services else []
        budgets = self.services.policies.list_budget_policies() if self.services else []
        agents = self.services.agents.list_agents() if self.services else []
        enterprise = self.services.enterprise_registry.list_apis() if self.services else []
        policy_lookups = self.services.policies.lookups() if self.services else {}
        enterprise_lookup = self._enterprise_lookup(enterprise)
        services = sorted({item.service_name for item in enterprise if item.status != "DELETED"})
        operations = sorted({item.operation for item in enterprise if item.status != "DELETED"})
        agent_statuses = ["ACTIVE", "SUSPENDED", "BLOCKED", "DELETED"]
        risk_tiers = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        return {
            **policy_lookups,
            **(self.services.enterprise_registry.lookups() if self.services else {}),
            "enterprise_apis": enterprise_lookup,
            "api_operations": [
                {"id": item.id, "service_name": item.service_name, "operation": item.operation, "status": item.status}
                for item in enterprise
            ],
            "governance_policies": [{"id": item.id, "policy_id": item.policy_id, "name": item.name, "enabled": item.enabled} for item in policies],
            "budget_policies": [{"id": item.id, "name": item.name, "department": item.department, "status": item.status} for item in budgets],
            "agent_passports": [{"id": item.id, "passport_id": item.passport_id, "name": item.name, "department": item.department} for item in agents],
            "versions": sorted({item.version for item in agents} | {item.version for item in enterprise}),
            "agent_statuses": agent_statuses,
            "risk_tiers": risk_tiers,
            "condition_value_options": {
                "identity.status": self._option_list(agent_statuses),
                "identity.department": self._option_list(policy_lookups.get("departments", [])),
                "identity.riskTier": self._option_list(risk_tiers),
                "normalizedExecution.service": self._option_list(services),
                "normalizedExecution.operation": self._option_list(operations),
                "risk.level": self._option_list(risk_tiers),
                "risk.category": self._option_list(risk_tiers),
            },
            "numeric_condition_fields": ["identity.trustScore", "normalizedExecution.amount", "risk.score"],
        }

    def _enterprise_lookup(self, enterprise: list) -> list[dict]:
        grouped: dict[str, set[str]] = {}
        for item in enterprise:
            if item.status == "DELETED":
                continue
            grouped.setdefault(item.service_name, set()).add(item.operation)
        return [
            {"service_name": service_name, "supported_operations": sorted(operations)}
            for service_name, operations in sorted(grouped.items())
        ]

    def _option_list(self, values: list[str]) -> list[dict[str, str]]:
        return [{"value": value, "label": value} for value in values]
