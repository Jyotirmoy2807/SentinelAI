from app.database.base import Base
from app.database.seed import seed_database
from app.database.session import SessionLocal, engine
from app import models  # noqa: F401


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
