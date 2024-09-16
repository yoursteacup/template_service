from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.models import DefaultModel


async def default_keeper(
        session: AsyncSession,
        query_parameter: str | None = None,
):
    if query_parameter:
        model = DefaultModel(query_parameter=query_parameter)
        session.add(model)
        await session.flush()
        await session.refresh(model)
        await session.commit()
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Saved {query_parameter} param with ID {model.id}"
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "No parameter passed"}
        )
