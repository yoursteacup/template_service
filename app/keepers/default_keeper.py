from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.models import DefaultModel
from app.schemas.default_schemas import DefaultSchema


async def get_parameter(
        session: AsyncSession,
        query_parameter: str | None = None,
):
    if query_parameter:
        record: DefaultModel = await DefaultModel.get_single_entity(
            session=session,
            filter_conditions=[DefaultModel.query_parameter == query_parameter]
        )
        if record:
            return JSONResponse(
                status_code=200,
                content={
                    "message": f"{record.query_parameter}"
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "message": "No records found"
                }
            )
    else:
        return JSONResponse(
            status_code=422,
            content={"message": "No parameter passed"}
        )


async def create_parameter(
        session: AsyncSession,
        request_schema: DefaultSchema,
):
    record = DefaultModel(
        query_parameter=request_schema.query_parameter
    )
    session.add(record)
    await session.flush()
    await session.refresh(record)
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": f"Saved with id {record.id}"}
    )
