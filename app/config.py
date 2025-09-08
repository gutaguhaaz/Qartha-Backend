from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MONGO_URL_ATLAS: str = os.getenv("MONGO_URL_ATLAS", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "qartha")
    BACKEND_BASE_URL: str = os.getenv("BACKEND_BASE_URL", f"https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost:5000')}")
    N8N_WEBHOOK_URL: str | None = os.getenv("N8N_WEBHOOK_URL")
    QRTIGER_API_KEY: str | None = os.getenv("QRTIGER_API_KEY")
    QRTIGER_API_BASE: str = os.getenv("QRTIGER_API_BASE", "https://api.qrcode-tiger.com")
    QRTIGER_DYNAMIC_PATH: str = os.getenv("QRTIGER_DYNAMIC_PATH", "/qr/dynamic")
    ALLOWED_ORIGINS: List[str] = (os.getenv("ALLOWED_ORIGINS", f"https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost:5000')},http://localhost:4200").split(","))

settings = Settings()
