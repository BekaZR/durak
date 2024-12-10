from typing import Any, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.cache_config import redis_client
from db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD:
    def __init__(self, session: AsyncSession | None = None):
        self.session = session
        self.redis = redis_client

    async def _update(
        self, db_obj: ModelType, update_data: dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        return db_obj
