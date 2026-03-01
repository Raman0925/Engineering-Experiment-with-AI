from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Config(BaseSettings):
    OpenAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore",env_file_required=False)


config = Config()