import asyncio

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from appmedica.database import setup_database
from appmedica.api import routers
from appmedica.service.mail_fetcher import mail_fetcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database_engine = setup_database()

    asyncio.create_task(mail_fetcher())

    for router in routers:
        app.include_router(router)

    yield


app = FastAPI(lifespan=lifespan)
