import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

load_dotenv()
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USERNAME')}" + \
    f":{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}" + \
    f":{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
