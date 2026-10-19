from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime config loaded from environment / `.env`.

    >>> Settings(  # doctest: +SKIP
    ...     database_url="postgresql+psycopg://x",
    ...     secret_key="unit-test-secret-key-with-at-least-32-chars",
    ... )
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    secret_key: str = Field(min_length=32)
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    environment: Literal["dev", "prod"] = "dev"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    @property
    def access_token_expire_seconds(self) -> int:
        return self.access_token_expire_minutes * 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
