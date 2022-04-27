from asyncio import sleep
from random import random
import numpy as np

from backend.app.dependencies.database import get_database
from backend.app.dependencies.repository import get_repository, Repository, RepositoryMap
from backend.app.models.ticker import TickerChange, Ticker
from backend.app.schemas.search import SearchSchema
from backend.app.schemas.ticker import TickerSchema


class TickerRefresher:
    def __init__(self):
        self.ticker_count = 100
        self.ticker_model = Repository(Ticker, get_database())
        self.ticker_change_model = Repository(TickerChange, get_database())

    @staticmethod
    def generate_movements():
        movements = np.random.choice(['1', '-1'], 100)
        return movements

    async def _create_tickers(self, start):
        ids = ',' . join([str(i) for i in range(start, self.ticker_count)])
        query = f'''
        INSERT INTO ticker(name, id, current_value)
        SELECT CONCAT('ticker_', id::CHAR), id::INTEGER, 0
        FROM    UNNEST(ARRAY[{ids}]::integer[]) as id
        '''
        await self.ticker_model.execute(query)

    async def init_tickers(self):
        tickers = await self.ticker_model.search(SearchSchema(page=0, limit=100))
        if len(tickers) < self.ticker_count:
            await self._create_tickers(start=len(tickers))

    async def create_tickers_changes(self, movements):
        movements = ','.join(movements)
        ids = ','.join([str(i) for i in range(0, self.ticker_count)])
        query = f'''
        INSERT INTO ticker_change(ticker_id, change_time, change_value)
        SELECT ticker_id::INTEGER, current_timestamp, move
        FROM    
        UNNEST(ARRAY[{ids}]::integer[]) as ticker_id,
        UNNEST(ARRAY[{movements}]) as move
        '''
        await self.ticker_change_model.execute(query)

    async def update_tickers(self, movements):
        movements = ','.join(movements)
        ids = ','.join([str(i) for i in range(0, self.ticker_count)])
        query = f'''
        update ticker 
        set current_value = current_value+data.move
        FROM (
        select 
        UNNEST(ARRAY[{ids}]::integer[]) as ticker_id,
        UNNEST(ARRAY[{movements}]) as move
        ) as data
        where id=data.ticker_id
        '''
        await self.ticker_model.execute(query)

    async def update_ticker_values(self):
        while True:
            movements = self.generate_movements()
            await self.create_tickers_changes(movements)
            await self.update_tickers(movements)
            await sleep(1)
