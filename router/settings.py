from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # ignore other envs from root .env
    )
    MASTER_AGENT_API_KEY: str = Field(
        default="e1adc3d8-fca1-40b2-b90a-7b48290f2d6a::master_server_ml",
        alias="MASTER_AGENT_API_KEY",
    )
    MASTER_BE_API_KEY: str = Field(
        default="7a3fd399-3e48-46a0-ab7c-0eaf38020283::master_server_be",
        alias="MASTER_BE_API_KEY",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get the settings object.

    Returns:
        Settings: The settings object.
    """
    return Settings()
