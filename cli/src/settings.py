from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    CLI_BACKEND_ORIGIN_URL: str = Field(default="http://localhost:8000")

    @field_validator("CLI_BACKEND_ORIGIN_URL")
    def check_for_trailing_slash(cls, v: str):
        if v.endswith("/"):
            raise ValueError(
                "'CLI_BACKEND_ORIGIN_URL' value must not have the trailing slash in the URL."
            )
        return v


@lru_cache
def get_settings():
    return Settings()
