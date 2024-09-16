# Template Service

## Components & Structure

### FastAPI

1. **app.routers** - Implement your own routes
2. **app.keepers** - Implement your logic for routes
3. **app.dependencies** - Implement your router dependencies
4. **app.services** - Implement your services

### SQLAlchemy & Alembic

1. **app.models.py** - Implement your own models
2. **alembic** - Your database migrations 

## Usage & Workflow

### Database & Models

1. Implement your models
2. Implement your `.env` from `.env.example`
3. Run `alembic revision --autogenerate -m "your revision name;"`
4. Run `chmod +x ./entrypoint.sh & ./entrypoint.sh` to migrate and start app or `alembic upgrade -head` to run migrations only

### Running Application

1. Just run `chmod +x ./entrypoint.sh & ./entrypoint.sh`