from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from src.restaurant.entity import RestaurantEntity


class RestaurantRepository:
	def __init__(self, database: AsyncIOMotorDatabase):
		self.database = database

	async def get_restaurants(
			self,
			category: str | None = None,
			district: str | None = None,
	) -> List[RestaurantEntity]:
		collection = self.database["restaurant"]

		# Build query only with provided filters; cast UUIDs to strings if stored as strings in Mongo.
		query: dict = {}
		if category is not None:
			query["category.id"] = category
		if district is not None:
			query["district.id"] = district
		# Exclude `_id` to avoid schema mismatch.
		cursor = collection.find(query)
		docs = await cursor.to_list(length=None)
		return [RestaurantEntity(**doc) for doc in docs]

	async def create_restaurant(self, restaurant_model: RestaurantEntity):
		collection = self.database["restaurant"]
		await collection.insert_one(
			{
				**restaurant_model.model_dump(by_alias=True, mode="json")
			}
		)

	async def get_restaurant_by_id(self, restaurant_id: str) -> RestaurantEntity | None:
		collection = self.database["restaurant"]
		doc = await collection.find_one({"_id": restaurant_id})
		if not doc:
			return None
		return RestaurantEntity(**doc)
