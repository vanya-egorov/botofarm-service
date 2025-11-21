from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database import engine, Base
from app.infrastructure.logging_config import logger
from app.handlers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start service")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Created databases")
    yield
    logger.info("Stop service")


app = FastAPI(
    title="Botofarm Service",
    description="""
    Все эндпоинты требуют авторизации.
    Используйте токен `admin-secret` в заголовке `Authorization: Bearer admin-secret`.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "botofarm-service"}

