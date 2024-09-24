from datetime import datetime
from typing import TypeVar

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

ModelType = TypeVar("ModelType", bound="Base")


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creation_date: Mapped[datetime] = mapped_column(insert_default=sa.func.now())
    update_date: Mapped[datetime] = mapped_column(insert_default=sa.func.now(), onupdate=func.now())

    @classmethod
    async def get_single_entity(
            cls,
            session: AsyncSession,
            filter_conditions: list[sa.ColumnElement] = None
    ) -> ModelType | None:
        result = await session.execute(sa.select(cls).where(*filter_conditions).limit(1))
        entity_tuple = result.first()
        if not entity_tuple:
            return None
        return entity_tuple[0]

    @classmethod
    async def get_entity_list(
            cls,
            session: AsyncSession,
            filter_conditions: list[sa.ColumnElement] = None
    ) -> list[ModelType] | None:
        if filter_conditions:
            result = await session.execute(sa.select(cls).where(*filter_conditions))
        else:
            result = await session.execute(sa.select(cls))
        result_list = list(result.scalars().all())
        if not result_list:
            return None
        return result_list


class DefaultModel(Base):
    __tablename__ = "default_model"

    query_parameter: Mapped[str] = mapped_column(nullable=True)
