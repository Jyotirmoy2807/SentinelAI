from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.container import ServiceContainer, build_service_container


def get_services(db: Session = Depends(get_db)) -> Generator[ServiceContainer, None, None]:
    yield build_service_container(db)
