from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.dependencies.token_dependency import token_dependency
from app.keepers import default_keeper
from app.schemas.default_schemas import DefaultSchema
from app.services.sessionmaking import get_session

router = APIRouter(
    prefix="/default",
    tags=["default"],
    dependencies=[Depends(token_dependency)],
)


@router.get("/{query_parameter}")
async def get_record(
        query_parameter: str | None,
        session: AsyncSession = Depends(get_session)
):
    return await default_keeper.get_parameter(
        session=session,
        query_parameter=query_parameter,
    )


@router.post("/")
async def create_record(
        request_schema: DefaultSchema,
        session: AsyncSession = Depends(get_session)
):
    return await default_keeper.create_parameter(
        session=session,
        request_schema=request_schema,
    )
