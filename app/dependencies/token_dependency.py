import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()


async def token_dependency(secret_key: str = Header(alias="x-api-key")) -> None:
    if secret_key != os.getenv("APP_SECRET_KEY"):
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"},
        )
