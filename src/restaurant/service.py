from datetime import datetime
from typing import List

from src.core.exceptions import BaseError
from src.core.utils import iso_to_24h_time
from src.restaurant.entity import RestaurantEntity
from src.restaurant.model import RestaurantFilter, RestaurantModel, RestaurantCreate, BaseRestaurantModel
from src.restaurant.repository import RestaurantRepository
from src.restaurant.utils import from_entity_to_model


class RestaurantService:
	"""Restaurant Service class."""

	def __init__(self, repository: RestaurantRepository):
		self.repository = repository

	async def get_list_owner_restaurant(self, owner_id: str) -> list[BaseRestaurantModel]:
		pass

	async def get_restaurants(self, request: RestaurantFilter) -> List[RestaurantModel] | None:
		try:
			data = await self.repository.filter_restaurant(
				district=request.district,
				category=request.category
			)
			return [from_entity_to_model(e) for e in data]
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
		openTime, closeTime = iso_to_24h_time(request.open_time), iso_to_24h_time(request.close_time)
		try:
			rate = request.rating
			if rate is None:
				rate = 5.0
			restaurant_entity = RestaurantEntity(
				name=request.name,
				address=request.address,
				image_url=request.image,
				openTime=openTime,
				closeTime=closeTime,
				district=request.district_id,
				categories=request.categories,
				rating=rate,
				created_at=datetime.utcnow(),
			)
			restaurant_entity.owner_id = owner_id
			await self.repository.create_restaurant(restaurant_entity)
			return True
		except Exception as e:
			print(e)
			raise

	async def update_restaurant(self, owner_id: str, restaurant_id, request: RestaurantCreate):
		openTime, closeTime = iso_to_24h_time(request.open_time), iso_to_24h_time(request.close_time)
		try:
			restaurant_entity = RestaurantEntity(
				restaurant_id=restaurant_id,
				name=request.name,
				address=request.address,
				image_url=request.image,
				openTime=openTime,
				closeTime=closeTime,
				district=request.district_id,
				categories=request.categories,
				rating=request.rating,
				created_at=datetime.utcnow(),
			)
			restaurant_entity.owner_id = owner_id
			await self.repository.update_restaurant(restaurant_id, restaurant_entity)
			return True
		except Exception as e:
			print(e)
			raise

	async def delete_restaurant(self, owner_id, restaurant_id):
		try:
			result = await self.repository.delete_restaurant(owner_id=owner_id, restaurant_id=restaurant_id)
			if result is False:
				raise BaseError(message="Delete restaurant fail")
		except Exception as e:
			raise

	async def get_admin_restaurants(self, admin_id) -> list[RestaurantModel]:
		try:
			data = await self.repository.get_admin_restaurants(admin_id=admin_id
			                                                   )
			return [from_entity_to_model(e) for e in data]
		except Exception:
			raise
