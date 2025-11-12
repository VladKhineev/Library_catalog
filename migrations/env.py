# migrations/env.py

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio

# ✅ Импортируем наш Base и модели, чтобы Alembic "видел" таблицы
from src.core.database import Base
from src.models.books_orm import BookORM  # важно импортировать, чтобы таблица не пропала из metadata

# Alembic Config — объект, который содержит настройки из alembic.ini
config = context.config

# ✅ Настройка логов Alembic (можно оставить без изменений)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Здесь Alembic узнаёт о структуре наших таблиц
target_metadata = Base.metadata


# === OFFLINE режим ===
# Используется для генерации SQL без подключения к БД
# Например: alembic upgrade head --sql
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# === ONLINE режим ===
# Используется при нормальной работе (с подключением к БД)
async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # ✅ Создаём асинхронный движок (asyncpg)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # не используем пул Alembic (FastAPI сам создаёт)
    )

    # ✅ Открываем подключение и выполняем миграции
    async with connectable.connect() as connection:

        # Важно: Alembic не async, поэтому "оборачиваем" миграции в run_sync
        await connection.run_sync(do_run_migrations)

    # Закрываем движок после выполнения миграций
    await connectable.dispose()


# Вспомогательная функция, которую Alembic вызовет в run_sync
def do_run_migrations(connection: Connection) -> None:
    """Sync migration logic (Alembic itself is sync)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # ✅ Эта опция позволяет Alembic сравнивать схемы и генерировать миграции
        compare_type=True,
        render_as_batch=True,  # нужно для SQLite, но полезно и для совместимости
    )

    with context.begin_transaction():
        context.run_migrations()


# ✅ Выбор режима: offline или online
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
