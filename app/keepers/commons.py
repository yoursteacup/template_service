import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy import ColumnElement

from typing import TypeVar
from typing import Type
from typing import List

ModelType = TypeVar("ModelType", bound="Base")


async def get_single_entity(
        *,
        session: AsyncSession,
        model: Type[ModelType],
        filter_conditions: list[ColumnElement] = None
) -> ModelType:
    result = await session.execute(select(model).where(*filter_conditions).limit(1))
    entity_tuple = result.first()
    if not entity_tuple:
        raise sqlalchemy.exc.NoResultFound(f"No result found for the query: {filter_conditions}")
    return entity_tuple[0]


async def get_entity_list(
        *,
        session: AsyncSession,
        model: Type[ModelType],
        filter_conditions: list[ColumnElement] = None,
) -> List[ModelType]:
    if filter_conditions:
        result = await session.execute(select(model).where(*filter_conditions))
    else:
        result = await session.execute(select(model))
    result_list = list(result.scalars().all())
    if not result_list:
        raise sqlalchemy.exc.NoResultFound(f"No result found for the query: {filter_conditions}")
    return result_list
