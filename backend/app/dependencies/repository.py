from __future__ import annotations

import functools
from typing import Generic, TypeVar, Type

import structlog
from databases import Database
from fastapi import Depends
from sqlalchemy import select, insert, update

from backend.app.dependencies.database import get_database
from backend.app.models.__meta__ import Base
from backend.app.schemas.__meta__ import Schema
from backend.app.schemas.search import SearchSchema

T = TypeVar("T", bound=Base)
V = TypeVar("V", bound=Schema)
logger = structlog.get_logger(__name__)


class RepositoryMap:
    mapping = dict()

    @classmethod
    def get(cls, model: Type[T]):
        return cls.mapping[model]

    @classmethod
    def set(cls, model: Type[T], repository: Type[Repository]):
        cls.mapping[model] = repository
        return cls

    @classmethod
    def has(cls, model: Type[T]):
        return model in cls.mapping


class Repository(Generic[T, V]):
    __model__ = None

    def __init__(self, model: Type[T], database: Database):
        self.model = model
        self.database = database

    async def execute(self, query, values: dict = None):
        return await self.database.execute(query, values)

    async def find(self, value) -> T:
        result = await self.database.fetch_one(query=select(self.model).where(self.model.id == value).order(id))
        return self.model(**result)

    async def find_one_by(self, field, value):
        result = await self.database.fetch_one(query=select(self.model).where(field == value))
        return self.model(**result)

    async def find_by(self, field, value, lazy: bool = True) -> list[T]:
        result = await self.database.fetch_all(query=select(self.model).where(field == value))
        return list(self.model(**row) for row in result)

    async def search(self, params: SearchSchema):
        query = select(self.model)
        query = self._with_search(query, params.filter)
        query = self._with_paging(query, params.page, params.limit)
        result = await self.database.fetch_all(query=query)
        return list(self.model(**row) for row in result)

    async def create(self, schema: V) -> T:
        result = await self.database.fetch_one(query=insert(self.model).values(**schema.dict()).returning(self.model))
        return self.model(**result)

    async def update(self, schema: V) -> T:
        result = await self.database.fetch_one(query=update(self.model).values(**schema.dict()).returning(self.model))
        return self.model(**result)

    def _with_paging(self, query, page, limit):  # noqa
        return query.offset(page * limit).limit(limit)

    def _with_search(self, query, where: dict):
        return query.where(*list(self.model[field].in_(values) for field, values in (where or dict()).items()))


def get_repository(model: Type[T]) -> Repository[T, V]:
    def _decorator(database: Database = Depends(get_database)):
        if not RepositoryMap.has(model):
            if inherited_cls := [cls for cls in Repository.__subclasses__() if cls.__model__ == model]:
                cls = inherited_cls[-1]
            else:
                cls = Repository
            logger.info(f"Setting repository to {RepositoryMap.__name__}", model=model, repository_cls=cls)
            RepositoryMap.set(model, cls)

        repo_type = RepositoryMap.get(model)
        return repo_type(model, database)

    return Depends(_decorator)
