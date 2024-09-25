#!/bin/sh

PROJECT_NAME=$(basename "$PWD")

mkdir -p app/routers app/keepers app/dependencies app/services app/schemas

cat <<EOT > requirements.txt
fastapi==0.114.2
python-dotenv==1.0.1
sqlalchemy==2.0.34
psycopg2-binary==2.9.9
alembic==1.13.2
uvicorn==0.30.6
asyncpg==0.29.0
EOT

cat <<EOT > entrypoint.sh
#!/bin/sh

alembic upgrade head
exec python -m app
EOT

cat <<EOT > .gitignore
.venv/
venv/
.idea/
__pycache__/

.env
EOT

cat <<EOT > .env.example
APP_PORT=8000
APP_ALLOWED_ORIGINS='["*"]'
APP_SECRET_KEY=r"^.{12,127}$"

POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USERNAME=$PROJECT_NAME
POSTGRES_PASSWORD=$PROJECT_NAME
POSTGRES_DATABASE=$PROJECT_NAME
POSTGRES_M_USERNAME=postgres
POSTGRES_M_PASSWORD=postgres
EOT

cat <<EOT > Dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
EOT

cat <<EOT > app/models.py
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
EOT

cat <<EOT > app/__main__.py
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
origins = json.loads(os.getenv("APP_ALLOWED_ORIGINS"))
app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == "__main__":
    import uvicorn  # noqa

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("APP_PORT")))

EOT

python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
alembic init alembic

ALEMBIC_ENV_FILE="./alembic/env.py"

if ! grep -q "load_dotenv()" "$ALEMBIC_ENV_FILE"; then
  echo "Adding import statements..."

  # Find the line number of the last 'import' or 'from ... import ...' statement
  last_import_line=$(grep -En "^(import|from .* import)" "$ALEMBIC_ENV_FILE" | tail -1 | cut -d: -f1)

  # Insert lines after the last import statement
  if [ -n "$last_import_line" ]; then
    sed -i "$((last_import_line + 1))i \\
import os\\
from dotenv import load_dotenv\\
\\
from app.models import Base\\
\\
load_dotenv()" "$ALEMBIC_ENV_FILE"
  else
    echo "No import statements found."
  fi
fi

if ! grep -q "DATABASE_URL = f" "$ALEMBIC_ENV_FILE"; then
  echo "Adding DATABASE_URL configuration..."

  # Find the line number containing 'config = context.config'
  config_line=$(grep -n "config = context.config" "$ALEMBIC_ENV_FILE" | cut -d: -f1)

  # Insert the DATABASE_URL and config.set_main_option after the found line
  if [ -n "$config_line" ]; then
    {
      echo 'DATABASE_URL = f"postgresql://{os.getenv('\''POSTGRES_USERNAME'\'')}" + \'
      echo '    f":{os.getenv('\''POSTGRES_PASSWORD'\'')}@{os.getenv('\''POSTGRES_HOST'\'')}" + \'
      echo '    f":{os.getenv('\''POSTGRES_PORT'\'')}/{os.getenv('\''POSTGRES_DATABASE'\'')}"'
      echo 'config.set_main_option("sqlalchemy.url", DATABASE_URL)'
    } | sed -i "$((config_line + 1))r /dev/stdin" "$ALEMBIC_ENV_FILE"
  else
    echo "'config = context.config' not found."
  fi
fi

if grep -q "target.metadata = None" "$ALEMBIC_ENV_FILE"; then
  echo "Replacing 'target.metadata = None' with 'target_metadata = Base.metadata'..."
  sed -i 's/target.metadata = None/target_metadata = Base.metadata/' "$ALEMBIC_ENV_FILE"
fi
