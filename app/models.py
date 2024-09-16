from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creation_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())


class DefaultModel(Base):
    __tablename__ = "default_model"

    query_parameter: Mapped[str] = mapped_column(nullable=True)