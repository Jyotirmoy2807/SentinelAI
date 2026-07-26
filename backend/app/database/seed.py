from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.approval import Approval
from app.models.audit_log import AuditLog
from app.models.enterprise_api import EnterpriseAPI
from app.models.governance_request import GovernanceRequest


def seed_database(db: Session) -> None:
    _seed_agents(db)
    _seed_enterprise_apis(db)
    _seed_demo_activity(db)
    db.commit()


def _table_has_rows(db: Session, model: type) -> bool:
    return db.scalars(select(model).limit(1)).first() is not None


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
                required_policies=["sentinelai/governance"],
                allowed_agents=["AGENT-REF-002"],
                endpoint_metadata={"owner": "Revenue Operations", "sla": "250ms mock"},
            ),
            EnterpriseAPI(
                service_name="Merchant Service",
                adapter="MerchantAdapter",
                version="1.8",
                status="ACTIVE",
                permissions=["lookup_merchant", "update_merchant"],
                required_policies=["sentinelai/governance"],
                allowed_agents=["AGENT-REF-002", "AGENT-MER-003"],
                endpoint_metadata={"owner": "Merchant Platform", "sla": "200ms mock"},
            ),
            EnterpriseAPI(
                service_name="Payment Service",
                adapter="PaymentAdapter",
                version="3.4",
                status="ACTIVE",
                permissions=["process_payment", "read_payment"],
                required_policies=["sentinelai/governance"],
                allowed_agents=["AGENT-INV-001", "AGENT-REF-002"],
                endpoint_metadata={"owner": "Treasury", "sla": "300ms mock"},
            ),
            EnterpriseAPI(
                service_name="Booking Service",
                adapter="BookingAdapter",
                version="1.3",
                status="ACTIVE",
                permissions=["confirm_booking", "cancel_booking"],
                required_policies=["sentinelai/governance"],
                allowed_agents=["AGENT-MER-003", "AGENT-BOOK-004"],
                endpoint_metadata={"owner": "Operations", "sla": "220ms mock"},
            ),
            EnterpriseAPI(
                service_name="Invoice Service",
                adapter="InvoiceAdapter",
                version="2.0",
                status="ACTIVE",
                permissions=["create_invoice", "read_invoice"],
                required_policies=["sentinelai/governance"],
                allowed_agents=["AGENT-INV-001"],
                endpoint_metadata={"owner": "Finance Systems", "sla": "280ms mock"},
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
            "graph_version": "v2",
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
        "risk": {"score": 36.38, "level": "LOW", "category": "LOW", "factors": []},
        "policy": {
            "decision": "REQUIRE_APPROVAL",
            "matched_policy": "sentinelai/governance/approval",
            "reasons": ["Transaction amount exceeds OPA approval threshold."],
        },
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
                reason="Transaction amount exceeds OPA approval threshold.",
                state_snapshot=paused_state,
                expires_at=now + timedelta(hours=6),
            ),
            AuditLog(
                event_id="EVT-SEED-001",
                request_id="REQ-SEED-APPROVAL",
                timestamp=now - timedelta(minutes=11),
                agent="Refund Agent",
                action="issue_refund",
                policy="sentinelai/governance/approval",
                risk_score=36.38,
                decision="REQUIRE_APPROVAL",
                approval_status="PENDING",
                latency_ms=211,
                reason="Refund request paused for human approval.",
                enterprise_api="Refund Service",
                stage="human_approval",
                payload={"amount": 875, "agent": "Refund Agent"},
                created_at=now - timedelta(minutes=11),
            ),
            AuditLog(
                event_id="EVT-SEED-002",
                request_id="REQ-SEED-ALLOW",
                timestamp=now - timedelta(hours=2),
                agent="Invoice Agent",
                action="create_invoice",
                policy="sentinelai/governance/allow",
                risk_score=22,
                decision="ALLOW",
                approval_status="NOT_REQUIRED",
                latency_ms=348,
                reason="Invoice creation approved and executed.",
                enterprise_api="Invoice Service",
                stage="audit_splunk",
                payload={"agent": "Invoice Agent"},
                created_at=now - timedelta(hours=2),
            ),
            AuditLog(
                event_id="EVT-SEED-003",
                request_id="REQ-SEED-DENY",
                timestamp=now - timedelta(hours=5),
                agent="IT Support Agent",
                action="delete_database",
                policy="sentinelai/governance/deny",
                risk_score=92,
                decision="DENY",
                approval_status="NOT_REQUIRED",
                latency_ms=96,
                reason="OPA denied destructive database instruction.",
                enterprise_api="Payroll Service",
                stage="policy_engine",
                payload={"policy": "sentinelai/governance/deny"},
                created_at=now - timedelta(hours=5),
            ),
        ]
    )
