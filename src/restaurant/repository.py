from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from src.restaurant.entity import RestaurantEntity


class RestaurantRepository:
	def __init__(self, database: AsyncIOMotorDatabase):
		self.database = database
		self.collection = database["restaurant"]

	async def filter_restaurant(
			self,
			category: int | None = None,
			district: int | None = None,
	) -> List[RestaurantEntity]:
		collection = self.database["restaurant"]

		# Build query only with provided filters; cast UUIDs to strings if stored as strings in Mongo.
		query: dict = {}
		if category:
			query["categories"] = category
		if district:
			query["district"] = district
		# Exclude `_id` to avoid schema mismatch.
		cursor = collection.find(query)
		docs = await cursor.to_list(length=None)
		return [RestaurantEntity(**doc) for doc in docs]
	async def get_admin_restaurants(
			self,
			admin_id: str,
	) -> List[RestaurantEntity]:
		collection = self.database["restaurant"]

		# Build query only with provided filters; cast UUIDs to strings if stored as strings in Mongo.
		query: dict = {"ownerId": admin_id}
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
		# Update due to change in mongo
		doc = await collection.find_one({"restaurant_id": restaurant_id})
		if not doc:
			return None
		return RestaurantEntity(**doc)

	async def update_restaurant(self, restaurant_id, restaurant_entity: RestaurantEntity):

		restaurant_dict = restaurant_entity.model_dump(by_alias=True)
		restaurant_dict.pop("_id", None)
		restaurant_dict.pop("id", None)
		result = await self.collection.update_one(
			{"restaurant_id": restaurant_id},
			{"$set": restaurant_dict}
		)
		return result.modified_count > 0

	async def delete_restaurant(self, restaurant_id,owner_id):
		result = await self.collection.delete_one(
			{"restaurant_id": restaurant_id, "ownerId": owner_id}
		)
		return result.deleted_count > 0
