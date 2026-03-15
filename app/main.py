from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import settings
from app.routers import chat, health, quick_actions
from app.utils.logger import get_logger
from app.utils.sync_employees import sync_employees_from_keycloak

logger = get_logger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting up chat service on port %s", settings.PORT)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        sync_employees_from_keycloak,
        trigger=IntervalTrigger(hours=1),
        id="sync_employees",
        name="Sync employees from Keycloak",
        replace_existing=True,
        misfire_grace_time=300,
    )
    scheduler.start()

    yield

    scheduler.shutdown()
    logger.info("Shutting down chat service")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Corporate Chat Bot API",
        description="Internal chat assistant for employees powered by LangGraph + RAGFlow",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(quick_actions.router)

    return app


app = create_app()
