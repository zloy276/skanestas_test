from starlette.middleware.cors import CORSMiddleware

from backend.app.events.ticker_events import TickerRefresher
from fastapi import FastAPI

from backend.app.dependencies.database import db
from backend.app.routes.ticker import ticker_router
from backend.config.settings import settings
from backend.utils.logger import RequestIdMiddleware, LOGGING_CONFIG


def append_routers(app: FastAPI) -> None:
    app.include_router(ticker_router)
    pass


def append_middlewares(app: FastAPI) -> None:
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def append_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup():
        await db.connect()

    @app.on_event("startup")
    async def startup():
        refresher = TickerRefresher()
        await refresher.init_tickers()
        # await refresher.update_ticker_values()

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(title="MediaSoft CRM")
    append_events(app)
    append_routers(app)
    append_middlewares(app)
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:create_app",
        host=settings.BIND_IP,
        port=8002,
        reload=True,
        factory=True,
        log_config=LOGGING_CONFIG,
    )
