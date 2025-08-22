""" Configuration settings for the FastAPI application."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the FastAPI application."""
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    postgres_password: str
    postgres_user: str
    postgres_db: str

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'local')}",
        env_file_encoding="utf-8"
        )


settings = Settings() # type: ignore
