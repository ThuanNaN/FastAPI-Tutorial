"""Cấu hình ứng dụng bằng pydantic-settings (12-factor) — topic 19 & 2.

Mọi biến môi trường được đọc từ .env. Không hardcode secret trong code.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FastAPI Bookstore"
    debug: bool = False

    database_url: str = "sqlite:///./bookstore.db"

    secret_key: str = "CHANGE-ME-KEY-EXTERNAL"  # ràng buộc: ≥ 32 ký tự
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    max_upload_size_mb: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()