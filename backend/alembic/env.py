from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import create_engine

from alembic import context

import app.models  # noqa: F401 — registra os models na metadata do Base
from app.core.config import get_settings
from app.core.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# DATABASE_URL vem de app.core.config (variável de ambiente), nunca do .ini
# nem passa pelo configparser do Alembic — a senha percent-encoded (%40 etc.)
# colide com a sintaxe de interpolação do configparser se for setada via
# config.set_main_option(), então a engine é criada direto aqui.
DATABASE_URL = get_settings().database_url

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
