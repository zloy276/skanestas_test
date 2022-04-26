from sqlalchemy import select
from typing import Optional, TypeVar

from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, ForeignKey
from fastapi import Depends
from backend.app.dependencies.database import get_database, Database

from backend.app.models.__meta__ import Base
from backend.app.schemas.__meta__ import Schema

T = TypeVar("T", bound=Base)
V = TypeVar("V", bound=Schema)


class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(BigInteger, primary_key=True, nullable=False, unique=True, index=True)

    name = Column(String(128), nullable=False)
    current_value = Column(Numeric, nullable=False, default=0)

    # async def fetch_all(self):
    #     result = await self.database.fetch_all(query=select(self.model))
    #     return list(self.model(**row) for row in result)


class TickerChange(Base):
    __tablename__ = "ticker_change"

    id = Column(BigInteger, primary_key=True, nullable=False, unique=True, index=True)

    ticker_id = Column(BigInteger, ForeignKey("ticker.id"))
    change_time = Column(DateTime, nullable=False)
    change_value = Column(Numeric, nullable=False)

    # async def get_last(self, ticker_id, count) -> Optional[T]:
    #     result = await self.database.fetch_all(
    #         query=select(self.model).where(ticker_id == ticker_id).count(count)
    #     )
    #     return list(self.model(**row) for row in result)
