from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.errors import BloomiError, bloomi_error_handler, unhandled_error_handler
from app.core.logging import configure_logging
from app.routers import checkins, companion, goals, home, journal, onboarding, shop


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Bloomi API",
        version="0.1.0",
        description="Compassionate self-care companion backend",
        docs_url="/docs" if not settings.is_prod else None,
        redoc_url="/redoc" if not settings.is_prod else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(BloomiError, bloomi_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_error_handler)

    app.include_router(onboarding.router)
    app.include_router(home.router)
    app.include_router(goals.router)
    app.include_router(checkins.router)
    app.include_router(companion.router)
    app.include_router(journal.router)
    app.include_router(shop.router)

    @app.get("/healthz", tags=["ops"])
    async def healthcheck() -> dict:
        return {"status": "ok", "service": "bloomi-api"}

    return app


app = create_app()
