import logging
from functools import cached_property

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    POOL_SIZE: int
    POOL_RECYCLE: int
    POOL_TIMEOUT: int
    MAX_OVERFLOW: int

    LOG_LEVEL: int = logging.INFO
    LOG_JSON: bool = False

    @cached_property
    def db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @classmethod
    @validator(
        "BIND_IP",
        "BIND_PORT",
        "DB_USER",
        "DB_PASS",
        "DB_HOST",
        "DB_PORT",
        "POOL_SIZE",
        "POOL_RECYCLE",
        "POOL_TIMEOUT",
        "MAX_OVERFLOW",
        pre=True,
    )
    def all_set(cls, values):
        if not all(map(lambda x: x is not None, values)):
            raise ValueError(values)
        return values

    class Config:
        env_file = "../../.env"
        keep_untouched = (cached_property,)
        arbitrary_types_allowed = True


settings = Settings()
