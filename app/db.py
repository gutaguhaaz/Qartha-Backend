from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URL_ATLAS) if settings.MONGO_URL_ATLAS else None

def get_db():
    if client is None:
        raise RuntimeError("MONGO_URL_ATLAS is not set. Configure your MongoDB connection string.")
    return client[settings.DATABASE_NAME]
