from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def client() -> TestClient:
    settings = Settings(
        database_url="postgresql+psycopg://bharatiq:test@localhost:5432/bharatiq",
        redis_url="redis://localhost:6379/0",
        frontend_origins=["http://localhost:5173"],
    )
    return TestClient(create_app(settings))


def test_health() -> None:
    response = client().get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "BharatIQ API"


def test_unavailable_market_is_never_live() -> None:
    response = client().get("/api/v1/markets/snapshots/nifty50")

    assert response.status_code == 200
    assert response.json()["symbol"] == "NIFTY50"
    assert response.json()["freshness"] == "UNAVAILABLE"


def test_invalid_market_symbol_is_rejected() -> None:
    response = client().get("/api/v1/markets/snapshots/NIFTY 50")

    assert response.status_code == 422


def test_cors_allows_the_configured_frontend_only() -> None:
    response = client().options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
