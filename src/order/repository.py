from motor.motor_asyncio import AsyncIOMotorDatabase

from src.order.entity import BookingEntity


class BookingRepository:
	def __init__(self, database: AsyncIOMotorDatabase):
		self.collection = database["booking"]

	async def create_booking(self, booking_entity: BookingEntity):
		await self.collection.insert_one(
			{
				**booking_entity.model_dump(by_alias=True, mode="json")
			}
		)

	async def get_user_booking_by_status(self, user_id: str, booking_status: int):
		query: dict = {"user_id": user_id}
		if booking_status:
			query["booking_status"] = booking_status
		cursor = self.collection.find(query, {"_id": 0})
		docs = await cursor.to_list(length=None)
		return [BookingEntity(**doc) for doc in docs]

	async def get_user_booking_by_restaurant_id(self, restaurant_id: str, booking_status: int):
		query: dict = {"restaurant_id": restaurant_id}
		if booking_status:
			query["booking_status"] = booking_status
		cursor = self.collection.find(query, {"_id": 0})
		docs = await cursor.to_list(length=None)
		return [BookingEntity(**doc) for doc in docs]

	async def get_booking_by_id(self, booking_id: str):
		doc = await self.collection.find_one({"booking_id": booking_id})
		if not doc:
			return None
		return BookingEntity(**doc)

	async def delete_booking(self, user_id, booking_id: str):
		result = await self.collection.delete_one({"booking_id": booking_id, "user_id": user_id})
		return result.deleted_count > 0

	async def update_booking_status(self, booking_id: str, booking_status: int):
		result = await self.collection.update_one(
			{"booking_id": booking_id},
			{"$set": {"booking_status": booking_status}}
		)
		return result.modified_count > 0

	async def update_booking(self, booking: BookingEntity):
		booking_dict = booking.model_dump(by_alias=True)
		booking_dict.pop("_id", None)
		booking_dict.pop("id", None)
		result = await self.collection.update_one(
			{"booking_id": booking.booking_id},
			{"$set": booking_dict}
		)
		return result.modified_count > 0
