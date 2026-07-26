from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.approval import Approval
from app.models.audit_log import AuditLog
from app.models.budget import BudgetProfile
from app.models.compliance_rule import ComplianceRule
from app.models.enterprise_api import EnterpriseAPI
from app.models.firewall_rule import FirewallRule
from app.models.governance_request import GovernanceRequest
from app.models.policy import Policy


def seed_database(db: Session) -> None:
    _seed_budgets(db)
    _seed_agents(db)
    _seed_enterprise_apis(db)
    _seed_policies(db)
    _seed_firewall_rules(db)
    _seed_compliance_rules(db)
    _seed_demo_activity(db)
    db.commit()


def _table_has_rows(db: Session, model: type) -> bool:
    return db.scalars(select(model).limit(1)).first() is not None


def _seed_budgets(db: Session) -> None:
    if _table_has_rows(db, BudgetProfile):
        return
    db.add_all(
        [
            BudgetProfile(
                name="Finance-Controlled",
                department="Finance",
                daily_limit=25000,
                monthly_limit=250000,
                transaction_limit=10000,
                approval_threshold=2000,
                spent_today=4200,
                spent_month=61300,
            ),
            BudgetProfile(
                name="Sales-Refunds",
                department="Sales",
                daily_limit=12000,
                monthly_limit=90000,
                transaction_limit=5000,
                approval_threshold=500,
                spent_today=1800,
                spent_month=22000,
            ),
            BudgetProfile(
                name="Operations-Standard",
                department="Operations",
                daily_limit=8000,
                monthly_limit=60000,
                transaction_limit=2500,
                approval_threshold=1200,
                spent_today=950,
                spent_month=9100,
            ),
            BudgetProfile(
                name="IT-Restricted",
                department="IT",
                daily_limit=2500,
                monthly_limit=20000,
                transaction_limit=800,
                approval_threshold=300,
                spent_today=200,
                spent_month=3700,
            ),
        ]
    )


def _seed_agents(db: Session) -> None:
    if _table_has_rows(db, Agent):
        return
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
                policy_groups=["default", "finance"],
                last_activity=datetime.utcnow() - timedelta(minutes=18),
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
                policy_groups=["default", "sales", "refunds"],
                last_activity=datetime.utcnow() - timedelta(minutes=42),
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
                policy_groups=["default", "operations"],
                last_activity=datetime.utcnow() - timedelta(hours=2),
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
                budget_profile="Operations-Standard",
                policy_groups=["default"],
                last_activity=datetime.utcnow() - timedelta(days=1),
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
                policy_groups=["default", "it"],
                last_activity=datetime.utcnow() - timedelta(days=3),
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
                permissions=["issue_refund", "read_refund"],
                required_policies=["POL-REF-500"],
                allowed_agents=["AGENT-REF-002"],
                endpoint_metadata={"owner": "Revenue Operations", "sla": "250ms mock"},
            ),
            EnterpriseAPI(
                service_name="Merchant Service",
                adapter="MerchantAdapter",
                version="1.8",
                status="ACTIVE",
                permissions=["lookup_merchant", "update_merchant"],
                required_policies=["POL-MER-OPS"],
                allowed_agents=["AGENT-REF-002", "AGENT-MER-003"],
                endpoint_metadata={"owner": "Merchant Platform", "sla": "200ms mock"},
            ),
            EnterpriseAPI(
                service_name="Payment Service",
                adapter="PaymentAdapter",
                version="3.4",
                status="ACTIVE",
                permissions=["process_payment", "read_payment"],
                required_policies=["POL-PAY-PCI"],
                allowed_agents=["AGENT-INV-001", "AGENT-REF-002"],
                endpoint_metadata={"owner": "Treasury", "sla": "300ms mock"},
            ),
            EnterpriseAPI(
                service_name="Booking Service",
                adapter="BookingAdapter",
                version="1.3",
                status="ACTIVE",
                permissions=["confirm_booking", "cancel_booking"],
                required_policies=["POL-OPS-BOOKING"],
                allowed_agents=["AGENT-MER-003", "AGENT-BOOK-004"],
                endpoint_metadata={"owner": "Operations", "sla": "220ms mock"},
            ),
            EnterpriseAPI(
                service_name="Invoice Service",
                adapter="InvoiceAdapter",
                version="2.0",
                status="ACTIVE",
                permissions=["create_invoice", "read_invoice"],
                required_policies=["POL-INV-FIN"],
                allowed_agents=["AGENT-INV-001"],
                endpoint_metadata={"owner": "Finance Systems", "sla": "280ms mock"},
            ),
        ]
    )


def _seed_policies(db: Session) -> None:
    if _table_has_rows(db, Policy):
        return
    db.add_all(
        [
            Policy(
                policy_id="POL-REF-500",
                name="Refunds Over 500 Require Review",
                description="Customer refunds over 500 require a human governance reviewer.",
                priority=10,
                department="Sales",
                policy_group="refunds",
                conditions={"service": "Refund Service", "operation": "issue_refund", "amount_greater_than": 500},
                actions={"decision": "REQUIRE_APPROVAL", "reason": "Refund amount exceeds the sales approval threshold."},
            ),
            Policy(
                policy_id="POL-REF-5000",
                name="Refunds Over 5000 Denied",
                description="Prototype limit that blocks unusually large automated refunds.",
                priority=5,
                department="Sales",
                policy_group="refunds",
                conditions={"service": "Refund Service", "operation": "issue_refund", "amount_greater_than": 5000},
                actions={"decision": "DENY", "reason": "Automated refunds above 5000 are not permitted."},
            ),
            Policy(
                policy_id="POL-PAY-PCI",
                name="PCI Governed Payment Processing",
                description="Payment execution must pass PCI and finance checks.",
                priority=15,
                department="Finance",
                policy_group="finance",
                conditions={"service": "Payment Service", "operation": "process_payment"},
                actions={"decision": "ALLOW", "reason": "Payment operation is governed by active PCI policy."},
            ),
            Policy(
                policy_id="POL-DEL-001",
                name="Block Autonomous Delete Operations",
                description="Delete operations are denied unless explicitly governed by a future workflow.",
                priority=1,
                department="Enterprise",
                policy_group="default",
                conditions={"operation": "delete_database"},
                actions={"decision": "DENY", "reason": "Delete database operations are prohibited for AI agents."},
            ),
            Policy(
                policy_id="POL-MER-OPS",
                name="Merchant Operations Boundary",
                description="Operations agents may update merchants when their passport includes the operation.",
                priority=25,
                department="Operations",
                policy_group="operations",
                conditions={"service": "Merchant Service", "operation": "update_merchant"},
                actions={"decision": "ALLOW", "reason": "Merchant update is inside the Operations policy boundary."},
            ),
        ]
    )


def _seed_firewall_rules(db: Session) -> None:
    if _table_has_rows(db, FirewallRule):
        return
    db.add_all(
        [
            FirewallRule(
                rule_id="FW-DESTRUCTIVE-001",
                name="Destructive Enterprise Instruction",
                category="Prompt Safety",
                severity="CRITICAL",
                pattern="delete database",
                blocked_operations=["delete_database", "disable_audit", "shutdown_system"],
                updated_by="security.admin",
            ),
            FirewallRule(
                rule_id="FW-BYPASS-002",
                name="Approval Bypass Attempt",
                category="Governance Bypass",
                severity="HIGH",
                pattern="bypass approval",
                updated_by="security.admin",
            ),
            FirewallRule(
                rule_id="FW-PAYROLL-003",
                name="Restricted Payroll Capability",
                category="Restricted API",
                severity="HIGH",
                blocked_services=["Payroll Service"],
                updated_by="compliance.admin",
            ),
        ]
    )


def _seed_compliance_rules(db: Session) -> None:
    if _table_has_rows(db, ComplianceRule):
        return
    db.add_all(
        [
            ComplianceRule(
                rule_id="COMP-PCI-001",
                name="PCI Payment Review",
                framework="PCI-DSS",
                affected_departments=["Finance", "Sales"],
                conditions={"service": "Payment Service", "amount_greater_than": 2000},
                require_approval=True,
            ),
            ComplianceRule(
                rule_id="COMP-SOC2-002",
                name="SOC2 High Risk Review",
                framework="SOC2",
                affected_departments=["All"],
                conditions={"risk_greater_than": 70},
                require_approval=True,
            ),
            ComplianceRule(
                rule_id="COMP-GDPR-003",
                name="GDPR Personal Data Guardrail",
                framework="GDPR",
                affected_departments=["HR", "Sales"],
                conditions={"operation": "export_personal_data", "decision": "FAIL"},
                require_approval=False,
            ),
        ]
    )


def _seed_demo_activity(db: Session) -> None:
    if _table_has_rows(db, GovernanceRequest):
        return
    now = datetime.utcnow()
    paused_state = {
        "request": {
            "raw": {
                "metadata": {"passportId": "AGENT-REF-002", "agentVersion": "1.0.0"},
                "execution": {
                    "service": "Refund Service",
                    "operation": "issue_refund",
                    "parameters": {"merchant_id": "MER-2049", "amount": 875, "reason": "duplicate charge"},
                },
            }
        },
        "metadata": {
            "request_id": "REQ-SEED-APPROVAL",
            "trace_id": "TRC-SEED-APPROVAL",
            "workflow_id": "WFL-SEED-APPROVAL",
            "graph_version": "v1",
            "timestamp": now.isoformat(),
        },
        "normalized_execution": {
            "passport_id": "AGENT-REF-002",
            "service": "Refund Service",
            "operation": "issue_refund",
            "parameters": {"merchant_id": "MER-2049", "amount": 875, "reason": "duplicate charge"},
            "amount": 875,
        },
        "identity": {
            "passport_id": "AGENT-REF-002",
            "agent_name": "Refund Agent",
            "department": "Sales",
            "status": "ACTIVE",
            "trust_score": 84,
            "reputation": 88,
            "allowed_apis": ["Refund Service"],
            "allowed_operations": ["issue_refund"],
            "policy_groups": ["default", "sales", "refunds"],
            "budget_profile": "Sales-Refunds",
            "decision": "ALLOW",
        },
        "policy": {"decision": "REQUIRE_APPROVAL", "reasons": ["Refund amount exceeds the sales approval threshold."]},
        "risk": {"score": 36.38, "category": "LOW", "factors": []},
        "budget": {"decision": "REQUIRE_APPROVAL", "reasons": ["Amount 875 exceeds approval threshold 500."]},
        "compliance": {"decision": "PASS", "approval_required": False, "reasons": ["Compliance checks passed."]},
        "approval": {
            "approval_id": "APR-SEED-001",
            "required": True,
            "status": "PENDING",
            "approver": "Governance Manager",
            "reason": "Refund amount exceeds the sales approval threshold.",
            "comments": "",
        },
        "events": [],
        "simulation": False,
    }
    db.add_all(
        [
            GovernanceRequest(
                request_id="REQ-SEED-APPROVAL",
                trace_id="TRC-SEED-APPROVAL",
                passport_id="AGENT-REF-002",
                service="Refund Service",
                operation="issue_refund",
                status="PENDING_APPROVAL",
                decision="REQUIRE_APPROVAL",
                risk_score=36.38,
                duration_ms=211,
                state_snapshot=paused_state,
            ),
            GovernanceRequest(
                request_id="REQ-SEED-ALLOW",
                trace_id="TRC-SEED-ALLOW",
                passport_id="AGENT-INV-001",
                service="Invoice Service",
                operation="create_invoice",
                status="APPROVED",
                decision="ALLOW",
                risk_score=22,
                duration_ms=348,
                completed_at=now - timedelta(hours=2),
            ),
            GovernanceRequest(
                request_id="REQ-SEED-DENY",
                trace_id="TRC-SEED-DENY",
                passport_id="AGENT-IT-005",
                service="Payroll Service",
                operation="delete_database",
                status="DENIED",
                decision="DENY",
                risk_score=92,
                duration_ms=96,
                completed_at=now - timedelta(hours=5),
            ),
            Approval(
                approval_id="APR-SEED-001",
                request_id="REQ-SEED-APPROVAL",
                passport_id="AGENT-REF-002",
                agent_name="Refund Agent",
                service="Refund Service",
                operation="issue_refund",
                amount=875,
                risk_score=36.38,
                approver="Governance Manager",
                status="PENDING",
                reason="Refund amount exceeds the sales approval threshold.",
                state_snapshot=paused_state,
                expires_at=now + timedelta(hours=6),
            ),
            AuditLog(
                audit_id="AUD-SEED-001",
                request_id="REQ-SEED-APPROVAL",
                event_type="APPROVAL_REQUIRED",
                node="human_approval",
                decision="REQUIRE_APPROVAL",
                message="Refund request paused for human approval.",
                payload={"amount": 875, "agent": "Refund Agent"},
                created_at=now - timedelta(minutes=11),
            ),
            AuditLog(
                audit_id="AUD-SEED-002",
                request_id="REQ-SEED-ALLOW",
                event_type="GOVERNANCE_DECISION",
                node="audit_engine",
                decision="ALLOW",
                message="Invoice creation approved and executed.",
                payload={"agent": "Invoice Agent"},
                created_at=now - timedelta(hours=2),
            ),
            AuditLog(
                audit_id="AUD-SEED-003",
                request_id="REQ-SEED-DENY",
                event_type="GOVERNANCE_DECISION",
                node="ai_firewall",
                decision="DENY",
                message="Firewall denied destructive database instruction.",
                payload={"rule": "FW-DESTRUCTIVE-001"},
                created_at=now - timedelta(hours=5),
            ),
        ]
    )
