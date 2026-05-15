from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BLOOMI_", env_file=".env", extra="ignore")

    env: Literal["dev", "staging", "prod"] = "dev"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/bloomi"
    secret_key: str = "change-me-in-production"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379/0"
    storage_bucket: str = "bloomi-assets"
    ai_provider: str = "anthropic"
    ai_model: str = "claude-haiku-4-5-20251001"
    ai_api_key: str = ""
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8081"]

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()
