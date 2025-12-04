from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    app_name: str = "File Organizer"
    version: str = "0.1.0"
    environment: str = Field("development", env="ENVIRONMENT")
    storage_dir: str = Field("./storage", env="STORAGE_DIR")
    supported_parsers: List[str] = Field(
        default_factory=lambda: ["text/plain", "application/json", "application/pdf"]
    )
    vector_dimensions: int = Field(384, env="VECTOR_DIMENSIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
