"""Application configuration loaded exclusively from environment variables."""
from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration shared by the API and background services."""

    app_environment: str = "development"
    app_name: str = "BharatIQ API"
    app_version: str = "0.1.0"
    frontend_origins: list[str] = ["http://localhost:5173"]
    database_url: str = "postgresql+psycopg://bharatiq:change-me@localhost:5432/bharatiq"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("frontend_origins", mode="before")
    @classmethod
    def split_frontend_origins(cls, value: object) -> object:
        """Accept a comma-separated environment value without allowing a wildcard."""
        if isinstance(value, str):
            origins = [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
            if "*" in origins:
                raise ValueError("FRONTEND_ORIGINS cannot contain '*' when credentials are enabled")
            return origins
        return value


@lru_cache
def get_settings() -> Settings:
    """Build and cache validated configuration once per process."""
    return Settings()
