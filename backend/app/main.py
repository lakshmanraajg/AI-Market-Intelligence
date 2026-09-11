"""Phase 1 API: health and source-safe market snapshot contracts."""
from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class Freshness(StrEnum):
    LIVE = "LIVE"
    DELAYED = "DELAYED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class Health(BaseModel):
    status: str = "ok"
    service: str
    version: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketSnapshot(BaseModel):
    symbol: str
    freshness: Freshness
    as_of: datetime | None = None
    provider: str | None = None
    message: str = "Data unavailable until an approved provider is configured."


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the API with CORS origins sourced from validated environment settings."""
    runtime_settings = settings or get_settings()
    app = FastAPI(
        title=runtime_settings.app_name,
        version=runtime_settings.app_version,
        docs_url="/api/docs",
        redoc_url=None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=runtime_settings.frontend_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

    @app.get("/health", response_model=Health, tags=["system"])
    def health() -> Health:
        return Health(service=runtime_settings.app_name, version=runtime_settings.app_version)

    @app.get(
        "/api/v1/markets/snapshots/{symbol}",
        response_model=MarketSnapshot,
        tags=["markets"],
    )
    def snapshot(
        symbol: Annotated[
            str,
            Path(
                min_length=1,
                max_length=40,
                pattern=r"^[A-Za-z0-9:_\-/]+$",
                description="Provider-normalized instrument symbol.",
            ),
        ],
    ) -> MarketSnapshot:
        """Return a safe empty state until a licensed provider is integrated."""
        return MarketSnapshot(symbol=symbol.upper(), freshness=Freshness.UNAVAILABLE)

    return app


app = create_app()
