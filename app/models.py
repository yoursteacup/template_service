import enum
from datetime import datetime
from typing import TypeVar

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


ModelType = TypeVar("ModelType", bound="Base")


class Serializable:
    def to_json(self, exclude=None):
        if exclude is None:
            exclude = []

        columns = {}
        for c in class_mapper(self.__class__).columns:
            if c.key not in exclude:
                value = getattr(self, c.key)

                # Convert datetime to ISO format
                if isinstance(value, datetime):
                    columns[c.key] = value.isoformat()
                else:
                    columns[c.key] = value

        return columns


class Base(DeclarativeBase, Serializable):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creation_date: Mapped[datetime] = mapped_column(insert_default=sa.func.now())
    update_date: Mapped[datetime] = mapped_column(insert_default=sa.func.now(), onupdate=sa.func.now())

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


class RequestLogs(Base):
    __tablename__ = "request_logs"

    method: Mapped[str] = mapped_column()
    endpoint: Mapped[str] = mapped_column()
    status_code: Mapped[int] = mapped_column()
    client_ip: Mapped[str] = mapped_column(nullable=True)
    proxy_ip: Mapped[str] = mapped_column(nullable=True)


class LogLevel(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class ApplicationLogs(Base):
    __tablename__ = "application_logs"

    message: Mapped[str] = mapped_column()
    level: Mapped[LogLevel] = mapped_column(sa.String)
    context: Mapped[str] = mapped_column()

