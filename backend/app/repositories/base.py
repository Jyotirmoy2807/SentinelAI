from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session


ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.db.scalars(statement).all())

    def get(self, entity_id: int) -> ModelT | None:
        return self.db.get(self.model, entity_id)

    def create(self, data: dict[str, Any]) -> ModelT:
        entity = self.model(**data)
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: ModelT, data: dict[str, Any]) -> ModelT:
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: ModelT) -> None:
        self.db.delete(entity)
        self.db.flush()
