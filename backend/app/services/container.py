from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.adapters.audit_sink import SQLiteSplunkAuditSink
from app.adapters.factory import EnterpriseAdapterFactory
from app.adapters.opa_adapter import OpaPolicyAdapter
from app.core.config import Settings, get_settings
from app.repositories.agent_repository import AgentRepository
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.budget_policy_repository import BudgetPolicyRepository
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.governance_policy_repository import GovernancePolicyRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository
from app.repositories.policy_deployment_repository import PolicyDeploymentRepository
from app.repositories.policy_version_repository import PolicyVersionRepository
from app.services.agent_service import AgentService
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService
from app.services.dashboard_service import DashboardService
from app.services.enterprise_api_registry_service import EnterpriseAPIRegistryService
from app.services.execution_service import ExecutionService
from app.services.explainability_service import ExplainabilityService
from app.services.ingestion_service import IngestionService
from app.services.normalization_service import NormalizationService
from app.services.policy_deployment_service import PolicyDeploymentService
from app.services.policy_service import PolicyService
from app.services.response_builder_service import ResponseBuilderService
from app.services.risk_service import RiskService
from app.services.settings_service import SettingsService


@dataclass
class ServiceContainer:
    settings: Settings
    adapter_factory: EnterpriseAdapterFactory
    ingestion: IngestionService
    normalization: NormalizationService
    agents: AgentService
    policies: PolicyService
    risk: RiskService
    approvals: ApprovalService
    execution: ExecutionService
    audit: AuditService
    explainability: ExplainabilityService
    response_builder: ResponseBuilderService
    dashboard: DashboardService
    enterprise_registry: EnterpriseAPIRegistryService
    settings_service: SettingsService


def build_service_container(db: Session) -> ServiceContainer:
    settings = get_settings()
    adapter_factory = EnterpriseAdapterFactory()
    agent_repository = AgentRepository(db)
    enterprise_repository = EnterpriseAPIRepository(db)
    approval_repository = ApprovalRepository(db)
    audit_repository = AuditRepository(db)
    request_repository = GovernanceRequestRepository(db)
    execution_repository = ExecutionRepository(db)
    governance_policy_repository = GovernancePolicyRepository(db)
    budget_policy_repository = BudgetPolicyRepository(db)
    policy_version_repository = PolicyVersionRepository(db)
    policy_deployment_repository = PolicyDeploymentRepository(db)
    audit_sink = SQLiteSplunkAuditSink(audit_repository)
    opa_adapter = OpaPolicyAdapter(settings.opa_url, settings.opa_decision_path, settings.request_timeout_seconds)
    policy_deployment = PolicyDeploymentService(
        governance_policy_repository,
        budget_policy_repository,
        policy_version_repository,
        policy_deployment_repository,
        settings.opa_policy_bundle_path,
    )

    container = ServiceContainer(
        settings=settings,
        adapter_factory=adapter_factory,
        ingestion=IngestionService(settings),
        normalization=NormalizationService(),
        agents=AgentService(agent_repository, enterprise_repository, budget_policy_repository, governance_policy_repository),
        policies=PolicyService(
            opa_adapter,
            governance_policy_repository,
            budget_policy_repository,
            policy_version_repository,
            policy_deployment,
        ),
        risk=RiskService(),
        approvals=ApprovalService(approval_repository),
        execution=ExecutionService(enterprise_repository, execution_repository, adapter_factory),
        audit=AuditService(audit_repository, request_repository, audit_sink),
        explainability=ExplainabilityService(),
        response_builder=ResponseBuilderService(),
        dashboard=DashboardService(
            agent_repository,
            governance_policy_repository,
            budget_policy_repository,
            enterprise_repository,
            approval_repository,
            request_repository,
            audit_repository,
        ),
        enterprise_registry=EnterpriseAPIRegistryService(enterprise_repository, adapter_factory, governance_policy_repository),
        settings_service=SettingsService(settings, adapter_factory, None),
    )
    container.settings_service.services = container
    return container
