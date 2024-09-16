from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.token_dependency import token_dependency
from app.keepers.default_keeper import default_keeper
from app.services.sessionmaking import get_session

router = APIRouter(
    prefix="/default",
    tags=["default"],
    dependencies=[Depends(token_dependency)],
)


@router.get("/{query_parameter}")
async def get_status(
        query_parameter: str | None,
        session: AsyncSession = Depends(get_session)
):
    return await default_keeper(
        session=session,
        query_parameter=query_parameter,
    )
