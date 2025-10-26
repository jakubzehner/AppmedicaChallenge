import asyncio

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from appmedica.logger import setup_logger

logger = setup_logger()

from appmedica.database import setup_database  # noqa: E402
from appmedica.api import routers  # noqa: E402
from appmedica.service.mail_fetcher import mail_fetcher  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database_engine = setup_database()

    asyncio.create_task(mail_fetcher())

    for router in routers:
        app.include_router(router)

    yield


app = FastAPI(lifespan=lifespan)
