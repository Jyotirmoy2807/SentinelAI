from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.budget_policy import BudgetPolicy
from app.models.enterprise_api import EnterpriseAPI
from app.models.governance_policy import GovernancePolicy
from app.utils.time import utc_now


def seed_database(db: Session) -> None:
    _seed_agents(db)
    _seed_enterprise_apis(db)
    _seed_governance_policies(db)
    _seed_budget_policies(db)
    db.commit()


def _table_has_rows(db: Session, model: type) -> bool:
    return db.scalars(select(model).limit(1)).first() is not None


def _seed_agents(db: Session) -> None:
    if _table_has_rows(db, Agent):
        return
    now = utc_now()
    db.add_all(
        [
            Agent(
                passport_id="AGENT-INV-001",
                name="Invoice Agent",
                owner="Maya Chen",
                department="Finance",
                status="ACTIVE",
                trust_score=92,
                reputation=95,
                risk_tier="LOW",
                allowed_apis=["Invoice Service", "Payment Service"],
                allowed_operations=["create_invoice", "read_invoice", "process_payment"],
                budget_profile="Finance-Controlled",
                policy_groups=["finance_amount_approval"],
                last_activity=now - timedelta(minutes=18),
            ),
            Agent(
                passport_id="AGENT-REF-002",
                name="Refund Agent",
                owner="Elena Brooks",
                department="Sales",
                status="ACTIVE",
                trust_score=84,
                reputation=88,
                risk_tier="MEDIUM",
                allowed_apis=["Refund Service", "Merchant Service", "Payment Service"],
                allowed_operations=["issue_refund", "lookup_merchant", "read_payment"],
                budget_profile="Sales-Refunds",
                policy_groups=["high_risk_approval"],
                last_activity=now - timedelta(minutes=42),
            ),
            Agent(
                passport_id="AGENT-MER-003",
                name="Merchant Agent",
                owner="Nikhil Rao",
                department="Operations",
                status="ACTIVE",
                trust_score=78,
                reputation=82,
                risk_tier="MEDIUM",
                allowed_apis=["Merchant Service", "Booking Service"],
                allowed_operations=["lookup_merchant", "update_merchant", "confirm_booking"],
                budget_profile="Operations-Standard",
                policy_groups=["destructive_action_deny"],
                last_activity=now - timedelta(hours=2),
            ),
            Agent(
                passport_id="AGENT-BOOK-004",
                name="Booking Agent",
                owner="Priya Shah",
                department="HR",
                status="SUSPENDED",
                trust_score=63,
                reputation=70,
                risk_tier="HIGH",
                allowed_apis=["Booking Service"],
                allowed_operations=["confirm_booking", "cancel_booking"],
                budget_profile="HR-Travel",
                policy_groups=["high_risk_approval"],
                last_activity=now - timedelta(days=1),
            ),
            Agent(
                passport_id="AGENT-IT-005",
                name="IT Support Agent",
                owner="Jon Bell",
                department="IT",
                status="BLOCKED",
                trust_score=45,
                reputation=54,
                risk_tier="HIGH",
                allowed_apis=["Merchant Service"],
                allowed_operations=["lookup_merchant"],
                budget_profile="IT-Restricted",
                policy_groups=["blocked_agent_deny"],
                last_activity=now - timedelta(days=3),
            ),
        ]
    )


def _seed_enterprise_apis(db: Session) -> None:
    if _table_has_rows(db, EnterpriseAPI):
        return
    db.add_all(
        [
            EnterpriseAPI(
                service_name="Refund Service",
                adapter="RefundAdapter",
                version="2.1",
                status="ACTIVE",
                supported_operations=["issue_refund", "read_refund"],
                required_policies=["high_risk_approval", "blocked_agent_deny"],
                endpoint_metadata={"owner": "Revenue Operations", "sla": "250ms mock"},
            ),
            EnterpriseAPI(
                service_name="Merchant Service",
                adapter="MerchantAdapter",
                version="1.8",
                status="ACTIVE",
                supported_operations=["lookup_merchant", "update_merchant"],
                required_policies=["blocked_agent_deny"],
                endpoint_metadata={"owner": "Merchant Platform", "sla": "200ms mock"},
            ),
            EnterpriseAPI(
                service_name="Payment Service",
                adapter="PaymentAdapter",
                version="3.4",
                status="ACTIVE",
                supported_operations=["process_payment", "read_payment"],
                required_policies=["high_risk_approval", "finance_amount_approval"],
                endpoint_metadata={"owner": "Treasury", "sla": "300ms mock"},
            ),
            EnterpriseAPI(
                service_name="Booking Service",
                adapter="BookingAdapter",
                version="1.3",
                status="ACTIVE",
                supported_operations=["confirm_booking", "cancel_booking"],
                required_policies=["blocked_agent_deny"],
                endpoint_metadata={"owner": "Operations", "sla": "220ms mock"},
            ),
            EnterpriseAPI(
                service_name="Invoice Service",
                adapter="InvoiceAdapter",
                version="2.0",
                status="ACTIVE",
                supported_operations=["create_invoice", "read_invoice"],
                required_policies=["finance_amount_approval"],
                endpoint_metadata={"owner": "Finance Systems", "sla": "280ms mock"},
            ),
        ]
    )


def _seed_governance_policies(db: Session) -> None:
    if _table_has_rows(db, GovernancePolicy):
        return
    db.add_all(
        [
            GovernancePolicy(
                policy_id="blocked_agent_deny",
                name="Blocked Agent Deny",
                description="Deny requests from blocked or unknown Agent Passports.",
                decision="DENY",
                priority=990000,
                enabled=True,
                conditions=[{"field": "identity.status", "operator": "not_equals", "value": "ACTIVE"}],
                reason="Agent Passport is not active.",
            ),
            GovernancePolicy(
                policy_id="destructive_action_deny",
                name="Destructive Action Deny",
                description="Deny destructive administrative actions.",
                decision="DENY",
                priority=980000,
                enabled=True,
                conditions=[{"field": "normalizedExecution.operation", "operator": "equals", "value": "delete_database"}],
                reason="Destructive database operations are forbidden.",
            ),
            GovernancePolicy(
                policy_id="high_risk_approval",
                name="High Risk Approval",
                description="Require human approval when NIST RMF risk exceeds the high-risk threshold.",
                decision="REQUIRE_APPROVAL",
                priority=880000,
                enabled=True,
                conditions=[{"field": "risk.score", "operator": "greater_or_equal", "value": 70}],
                reason="High NIST RMF risk score requires human approval.",
            ),
            GovernancePolicy(
                policy_id="finance_amount_approval",
                name="Finance Amount Approval",
                description="Require approval for high-value finance transactions.",
                decision="REQUIRE_APPROVAL",
                priority=870000,
                enabled=True,
                conditions=[
                    {"field": "identity.department", "operator": "equals", "value": "Finance"},
                    {"field": "normalizedExecution.amount", "operator": "greater_or_equal", "value": 5000},
                ],
                reason="Finance transaction amount requires governance approval.",
            ),
        ]
    )


def _seed_budget_policies(db: Session) -> None:
    if _table_has_rows(db, BudgetPolicy):
        return
    db.add_all(
        [
            BudgetPolicy(
                name="Finance-Controlled",
                department="Finance",
                daily_limit=25000,
                monthly_limit=250000,
                transaction_limit=10000,
                approval_threshold=5000,
                spent_today=0,
                spent_month=0,
                status="ACTIVE",
            ),
            BudgetPolicy(
                name="Sales-Refunds",
                department="Sales",
                daily_limit=15000,
                monthly_limit=150000,
                transaction_limit=5000,
                approval_threshold=750,
                spent_today=0,
                spent_month=0,
                status="ACTIVE",
            ),
            BudgetPolicy(
                name="Operations-Standard",
                department="Operations",
                daily_limit=12000,
                monthly_limit=100000,
                transaction_limit=4000,
                approval_threshold=1500,
                spent_today=0,
                spent_month=0,
                status="ACTIVE",
            ),
            BudgetPolicy(
                name="HR-Travel",
                department="HR",
                daily_limit=8000,
                monthly_limit=60000,
                transaction_limit=3000,
                approval_threshold=1000,
                spent_today=0,
                spent_month=0,
                status="ACTIVE",
            ),
            BudgetPolicy(
                name="IT-Restricted",
                department="IT",
                daily_limit=2500,
                monthly_limit=20000,
                transaction_limit=1000,
                approval_threshold=500,
                spent_today=0,
                spent_month=0,
                status="ACTIVE",
            ),
        ]
    )
