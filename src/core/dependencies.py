from typing import AsyncGenerator

import redis
from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.asynchronous.database import AsyncDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.core.config import settings


# Mongo Dependencies

# 1. Mongo
def get_client(request: Request) -> AsyncDatabase:
	return request.app.state.mongo_client


def get_mongo_db(mongo_client: AsyncDatabase = Depends(get_client)) -> AsyncIOMotorDatabase:
	"""Inject the default database."""
	return mongo_client.get_database(settings.MONGO_DATABASE)

#Inject this in dependencies
def get_collection(collection_name: str):
	"""Get a specific collection by name."""

	def _get_collection(db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> AsyncIOMotorCollection:
		return db[collection_name]

	return _get_collection


# 2. Postgres
postgres_engine = create_async_engine(
	settings.POSTGRES_CONNECTION_URL,  # Fixed: was TEST_DATABASE_URL
	# connect_args={"options": "-c timezone=UTC"},
	echo=False,  # Set True to see SQL logs
	pool_pre_ping=True,  # Verify connections before using them
	pool_size=10,  # Maximum number of connections to keep in the pool
	max_overflow=20,  # Maximum overflow connections
)
Session = async_sessionmaker(
	bind=postgres_engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autocommit=False,
	autoflush=False,
)

#Inject this in dependencies
async def get_session() -> AsyncGenerator[AsyncSession, None]:
	async with Session() as session:
		try:
			yield session
			await session.commit()
		except Exception:
			await session.rollback()
			raise
# 3. Redis
def get_redis_client():
	return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, username=settings.REDIS_USERNAME,
	                   password=settings.REDIS_PASSWORD, decode_responses=True)
