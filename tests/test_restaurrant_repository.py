import pytest
from pymongo import AsyncMongoClient

from src.core.config import settings
from src.restaurant.repository import RestaurantRepository





@pytest.mark.asyncio
async def test_get_restaurant():
	mongo_client = AsyncMongoClient(settings.MONGO_URI)
	database = mongo_client.get_database(settings.MONGO_DATABASE)
	restaurant_repsository = RestaurantRepository(database=database)
	data = await restaurant_repsository.get_restaurants(owner_id="7bcb12fd-38b5-4080-9686-6d52165a3045")
	print(data)


