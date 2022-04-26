from asyncio import sleep

from fastapi import APIRouter, status, WebSocket
from typing import List

from backend.app.dependencies.repository import Repository, get_repository
from backend.app.models.ticker import Ticker, TickerChange
from backend.app.schemas.search import SearchSchema
from backend.app.schemas.ticker import TickerChangeSchema, TickerSchema
from fastapi.encoders import jsonable_encoder


ticker_router = APIRouter()


@ticker_router.websocket("/ticker/{ticker_id}/ws")
async def ticker_websocket(
        websocket: WebSocket,
        ticker_id: int,
        repository: Repository = get_repository(TickerChange),
        page: int = 0,
        limit: int = 25
):
    await websocket.accept()
    data = await repository.search(SearchSchema(page=page, limit=limit))
    # await websocket.send_json(data)
    while True:
        # await websocket.send_json(data)
        await websocket.send_json({'123': jsonable_encoder(data)})
        await sleep(2)


@ticker_router.get("/ticker/", response_model=List[TickerSchema], status_code=status.HTTP_200_OK)
async def get_employee_with_paging(page: int = 0, limit: int = 25, repository: Repository = get_repository(Ticker)):
    result = await repository.search(SearchSchema(page=page, limit=limit))
    return result
