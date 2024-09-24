# Шаблон сервиса

$\color{red}{Составлено} \space {Даулетом.}$

$\color{green}{Одобрено} \space {Эльдаром.}$

$\color{green}{Согласна} \space {Ника.}$


## Компоненты и структура

### FastAPI

1. **./app/routers/** - Реализуйте свои маршруты
2. **./app/keepers/** - Реализуйте свою логику для маршрутов
3. **./app/dependencies/** - Реализуйте зависимости для маршрутов
4. **./app/services/** - Реализуйте свои сервисы

### SQLAlchemy & Alembic

1. **./app/models.py** - Реализуйте свои модели
2. **./alembic** - Ваши миграции базы данных

## Использование и рабочий процесс

### База данных и модели

1. Реализуйте свои модели
2. Настройте файл `.env` на основе `.env.example`
3. Выполните команду `alembic revision --autogenerate -m "название вашей ревизии";`
4. Выполните `chmod +x ./entrypoint.sh & ./entrypoint.sh` для миграции и запуска приложения или `alembic upgrade -head` для запуска только миграций

### Запуск приложения

1. Просто выполните команду `chmod +x ./entrypoint.sh & ./entrypoint.sh`

# Как создать проект по шаблону

1. Создать структуру:
```
./app/dependencies/
./app/keepers/
./app/routers/
./app/schemas/
./app/services/
```

2. Скопировать файлы:
```
./requirements.txt
./entrypoint.sh
./gitignore
./.env.example
./Dockerfile
./app/models.py
./app/__main__.py
```

3. В контексте виртуального окружения выполнить команды:

 - ``pip install -r requirements.txt``

 - ``alembic init alembic``

4. Внести правки в файл ``./alembic/env.py``

 - После импортов добавить строки:
```
import os
from dotenv import load_dotenv
from app.models import Base

load_dotenv()
```

 - После строки ``config = context.config`` добавить строки:
```
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USERNAME')}" + \
    f":{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}" + \
    f":{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}"
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

 - Строку ``target_metadata = None`` заменить на ``target_metadata = Base.metadata``
