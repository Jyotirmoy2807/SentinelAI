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
    if "audit_logs" not in inspector.get_table_names():
        return
    audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
    if "event_id" in audit_columns:
        return
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE audit_logs"))
