"""Phase 1 foundation API: health, versioned routing and source-safe market contract."""
from datetime import UTC, datetime
from enum import StrEnum
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="BharatIQ API", version="0.1.0", docs_url="/api/docs")
class Freshness(StrEnum): LIVE="LIVE"; DELAYED="DELAYED"; STALE="STALE"; UNAVAILABLE="UNAVAILABLE"
class Health(BaseModel): status: str = "ok"; timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
class MarketSnapshot(BaseModel):
    symbol: str; freshness: Freshness; as_of: datetime | None = None; provider: str | None = None
    message: str = "Data unavailable until an approved provider is configured."
@app.get("/health", response_model=Health, tags=["system"])
def health() -> Health: return Health()
@app.get("/api/v1/markets/snapshots/{symbol}", response_model=MarketSnapshot, tags=["markets"])
def snapshot(symbol: str) -> MarketSnapshot: return MarketSnapshot(symbol=symbol.upper(), freshness=Freshness.UNAVAILABLE)
