from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.adapters.factory import EnterpriseAdapterFactory
from app.core.config import Settings, get_settings
from app.repositories.agent_repository import AgentRepository
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.budget_repository import BudgetRepository
from app.repositories.compliance_repository import ComplianceRepository
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.firewall_repository import FirewallRepository
from app.repositories.governance_decision_repository import GovernanceDecisionRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository
from app.repositories.policy_repository import PolicyRepository
from app.services.agent_service import AgentService
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService
from app.services.budget_service import BudgetService
from app.services.compliance_service import ComplianceService
from app.services.dashboard_service import DashboardService
from app.services.enterprise_api_registry_service import EnterpriseAPIRegistryService
from app.services.execution_service import ExecutionService
from app.services.explainability_service import ExplainabilityService
from app.services.firewall_service import FirewallService
from app.services.ingestion_service import IngestionService
from app.services.normalization_service import NormalizationService
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
    firewall: FirewallService
    risk: RiskService
    budget: BudgetService
    compliance: ComplianceService
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
    policy_repository = PolicyRepository(db)
    firewall_repository = FirewallRepository(db)
    budget_repository = BudgetRepository(db)
    compliance_repository = ComplianceRepository(db)
    enterprise_repository = EnterpriseAPIRepository(db)
    approval_repository = ApprovalRepository(db)
    audit_repository = AuditRepository(db)
    request_repository = GovernanceRequestRepository(db)
    execution_repository = ExecutionRepository(db)
    decision_repository = GovernanceDecisionRepository(db)

    return ServiceContainer(
        settings=settings,
        adapter_factory=adapter_factory,
        ingestion=IngestionService(settings),
        normalization=NormalizationService(),
        agents=AgentService(agent_repository),
        policies=PolicyService(policy_repository),
        firewall=FirewallService(firewall_repository),
        risk=RiskService(),
        budget=BudgetService(budget_repository),
        compliance=ComplianceService(compliance_repository),
        approvals=ApprovalService(approval_repository),
        execution=ExecutionService(enterprise_repository, execution_repository, adapter_factory),
        audit=AuditService(audit_repository, request_repository, decision_repository),
        explainability=ExplainabilityService(),
        response_builder=ResponseBuilderService(),
        dashboard=DashboardService(
            agent_repository,
            policy_repository,
            enterprise_repository,
            approval_repository,
            request_repository,
            audit_repository,
        ),
        enterprise_registry=EnterpriseAPIRegistryService(enterprise_repository),
        settings_service=SettingsService(settings, adapter_factory),
    )
