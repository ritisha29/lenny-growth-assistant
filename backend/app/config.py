from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# lenny-growth-assistant/
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str

    llm_provider: str = "ollama"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    anthropic_api_key: str | None = None

    app_env: str = "development"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()