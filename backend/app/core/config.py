from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareerLens API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = Field(
        default="postgresql+asyncpg://careerlens:careerlens@localhost:5432/careerlens",
        description="Async SQLAlchemy PostgreSQL URL",
    )

    log_level: str = "INFO"
    allowed_origins: str = "http://localhost:3000"

    # Authentication compatibility settings.
    secret_key: str = Field(default="change-me-in-development", min_length=16)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, ge=5, le=1440)

    # AI is provider-agnostic and OpenAI-compatible by design.
    ai_enabled: bool = False
    ai_provider: str = "openai_compatible"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_model: str = "gpt-5-mini"
    ai_timeout_seconds: float = Field(default=30.0, gt=0, le=120)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
