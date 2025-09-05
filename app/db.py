from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import certifi
import logging

logger = logging.getLogger(__name__)

def create_client():
    if not settings.MONGO_URL_ATLAS:
        logger.warning("MONGO_URL_ATLAS not configured")
        return None
    
    try:
        # MongoDB Atlas connection with SSL/TLS configuration
        client = AsyncIOMotorClient(
            settings.MONGO_URL_ATLAS,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,  # 5 seconds timeout
            maxPoolSize=10,
            retryWrites=True
        )
        return client
    except Exception as e:
        logger.error(f"Failed to create MongoDB client: {e}")
        return None

client = create_client()

def get_db():
    if client is None:
        raise RuntimeError(
            "MongoDB connection not available. Please configure MONGO_URL_ATLAS in your environment variables."
        )
    return client[settings.DATABASE_NAME]
