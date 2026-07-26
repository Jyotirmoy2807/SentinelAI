from sqlalchemy import inspect, text

from app.database.base import Base
from app.database.seed import seed_database
from app.database.session import SessionLocal, engine
from app import models  # noqa: F401


def init_database() -> None:
    _migrate_prototype_schema()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


def _migrate_prototype_schema() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    with engine.begin() as connection:
        audit_dropped = False
        if "audit_logs" in table_names:
            audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
            if "event_id" not in audit_columns:
                connection.execute(text("DROP TABLE audit_logs"))
                audit_dropped = True

        if "enterprise_apis" in table_names:
            enterprise_columns = {column["name"] for column in inspector.get_columns("enterprise_apis")}
            if "supported_operations" not in enterprise_columns or "permissions" in enterprise_columns or "allowed_agents" in enterprise_columns:
                connection.execute(text("DROP TABLE enterprise_apis"))

        if "governance_requests" in table_names:
            connection.execute(text("DELETE FROM governance_requests WHERE request_id LIKE 'REQ-SEED-%'"))
        if "approvals" in table_names:
            connection.execute(text("DELETE FROM approvals WHERE approval_id LIKE 'APR-SEED-%'"))
        if "audit_logs" in table_names and not audit_dropped:
            connection.execute(text("DELETE FROM audit_logs WHERE event_id LIKE 'EVT-SEED-%'"))
        if "agents" in table_names:
            connection.execute(text("""UPDATE agents SET policy_groups = '["finance_amount_approval"]' WHERE passport_id = 'AGENT-INV-001'"""))
            connection.execute(text("""UPDATE agents SET policy_groups = '["high_risk_approval"]' WHERE passport_id = 'AGENT-REF-002'"""))
            connection.execute(text("""UPDATE agents SET policy_groups = '["destructive_action_deny"]' WHERE passport_id = 'AGENT-MER-003'"""))
            connection.execute(text("""UPDATE agents SET policy_groups = '["high_risk_approval"]', budget_profile = 'HR-Travel' WHERE passport_id = 'AGENT-BOOK-004'"""))
            connection.execute(text("""UPDATE agents SET policy_groups = '["blocked_agent_deny"]' WHERE passport_id = 'AGENT-IT-005'"""))
