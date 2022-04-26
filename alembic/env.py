from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from backend.app.models.__meta__ import Base
from backend.app.models.ticker import Ticker  # noqa
from backend.config.settings import settings

config = context.config
target_metadata = Base.metadata

config.set_main_option("DB_USER", settings.DB_USER)
config.set_main_option("DB_PASS", settings.DB_PASS)
config.set_main_option("DB_HOST", settings.DB_HOST)
config.set_main_option("DB_PORT", settings.DB_PORT)
config.set_main_option("DB_NAME", settings.DB_NAME)


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
