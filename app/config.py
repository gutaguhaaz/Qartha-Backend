from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MONGO_URL_ATLAS: str = os.getenv("MONGO_URL_ATLAS", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "qartha")
    BACKEND_BASE_URL: str = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    N8N_WEBHOOK_URL: str | None = os.getenv("N8N_WEBHOOK_URL")
    QRTIGER_API_KEY: str | None = os.getenv("QRTIGER_API_KEY")
    ALLOWED_ORIGINS: List[str] = (os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(","))

settings = Settings()
