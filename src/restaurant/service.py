from datetime import datetime
from typing import List

from src.restaurant.entity import DistrictEntity, CategoryEntity
from src.restaurant.entity import RestaurantEntity
from src.restaurant.model import RestaurantFilter, RestaurantModel, District, Category, RestaurantCreate
from src.restaurant.repository import RestaurantRepository


class RestaurantService:
	"""Restaurant Service class."""

	def __init__(self, repository: RestaurantRepository):
		self.repository = repository

	async def get_restaurants(self, request: RestaurantFilter) -> List[RestaurantModel] | None:
		try:
			data: list[RestaurantEntity] = await self.repository.get_restaurants(request.category, request.district)
			list_restaurants = []
			if data is None:
				return list_restaurants
			for entity in data:
				restaurant = from_entity_to_model(entity=entity)

				list_restaurants.append(restaurant)
			return list_restaurants
		except Exception:
			raise

	async def get_restaurant_by_id(self, restaurant_id: str):
		try:
			data = await self.repository.get_restaurant_by_id(restaurant_id)
			if data is None:
				return {}

			restaurant = from_entity_to_model(entity=data)
			return restaurant
		except Exception:
			raise

	async def create_restaurant(self, owner_id: str, request: RestaurantCreate):

		try:
			categories = [CategoryEntity(**c.model_dump(by_alias=True)) for c in request.categories]
			restaurant_entity = RestaurantEntity(
				name=request.name,
				address=request.address,
				image_url=request.image,
				openTime=request.open_time,
				closeTime=request.close_time,
				district=DistrictEntity(**request.district.model_dump()),
				categories=categories,
				rating=2.0,
				created_at=datetime.utcnow(),
			)
			restaurant_entity.owner_id = owner_id
			await self.repository.create_restaurant(restaurant_entity)
			return True
		except Exception as e:
			print(e)
			raise


def from_entity_to_model(entity: RestaurantEntity) -> RestaurantModel:
	open_time: str = entity.openTime.strftime("%H:%M")
	close_time: str = entity.closeTime.strftime("%H:%M")
	categories = [Category(**c.model_dump()) for c in entity.categories]
	restaurant = RestaurantModel(restaurantId=entity.id, name=entity.name, address=entity.address,
	                             picture=entity.image, rating=entity.rating, openTime=open_time,
	                             closeTime=close_time, district=District(**entity.district.model_dump()),
	                             categories=categories)
	return restaurant
