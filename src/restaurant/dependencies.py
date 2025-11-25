from fastapi import Depends

from src.core.dependencies import get_mongo_db
from src.restaurant.repository import RestaurantRepository
from src.restaurant.service import RestaurantService


def get_restaurant_service(database=Depends(get_mongo_db)):
	repository = RestaurantRepository(database=database)
	return RestaurantService(repository)