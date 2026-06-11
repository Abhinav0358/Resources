import os

import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --- PostgreSQL Configuration (Async) ---
POSTGRES_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://admin:password123@postgres:5432/vision_db"
)
engine = create_async_engine(POSTGRES_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# --- MongoDB Configuration (Async) ---
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client.vision_events

# --- Redis Configuration (Async) ---
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


# Dependency to get Postgres session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
