from functools import lru_cache

from databases import Database

from backend.config.settings import settings

db = Database(settings.db_url)


@lru_cache
def get_database() -> Database:
    return db
