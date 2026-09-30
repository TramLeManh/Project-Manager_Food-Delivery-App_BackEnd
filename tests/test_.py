import uuid

import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.core.config import settings

# === Global variable ===
test_user_id: uuid.UUID = "339591b8-99a7-4ffd-8e4e-bd1ac2e5d778"

# === Config database ===
DATABASE_URL = settings.POSTGRES_CONNECTION_URL
postgres_engine = create_async_engine(
	DATABASE_URL,  # Fixed: was TEST_DATABASE_URL
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


# 1. Test session. Commit here will not save in database
@pytest_asyncio.fixture(scope="function")
async def get_test_session():
	async with postgres_engine.connect() as connection:
		# Start a SAVEPOINT transaction
		trans = await connection.begin()
		# Make a SQLAlchemy session
		async_session = Session(bind=connection)
		try:
			# Provide session for repository
			yield async_session
		finally:
			# Rollback all operations to revert changes
			await trans.rollback()
			await async_session.close()


# 2. Real session. Commit here will store in database
@pytest_asyncio.fixture(scope="function")
async def get_real_session():
	#Note do not use this product
	async with postgres_engine.connect() as connection:
		# Start a SAVEPOINT transaction
		trans = await connection.begin()
		# Make a SQLAlchemy session
		async_session = Session(bind=connection)
		try:
			yield async_session
			# Commit all operations after the test completes successfully
			await trans.commit()
		except Exception:
			# If the test failed, rollback to keep DB consistent
			await trans.rollback()
			raise
		finally:
			# Always close the session
			await async_session.close()
#3. MongoDb
@pytest.fixture()
def mongo_database():
	mongo_client = AsyncMongoClient(settings.MONGO_URI)
	return mongo_client.get_database(settings.MONGO_DATABASE)

