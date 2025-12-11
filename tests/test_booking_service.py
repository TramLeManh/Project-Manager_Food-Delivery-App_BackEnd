from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from src.core.config import settings
from src.order.exception import BookingError, DeleteBookingError
from src.order.model import BookingCreate
from src.order.repository import BookingRepository
from src.order.service import BookingService
from src.restaurant.repository import RestaurantRepository


@pytest.fixture()
def get_database() -> AsyncIOMotorDatabase:
	mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
	return mongo_client.get_database(settings.MONGO_DATABASE)


@pytest.fixture()
def booking_service(get_database):
	booking_repository = BookingRepository(get_database)
	restaurant_repository = RestaurantRepository(get_database)
	from src.auth.service_email import EmailService
	booking_service = BookingService(booking_repository=booking_repository, restaurant_repository=restaurant_repository,
	                                 email_service=EmailService())
	return booking_service


@pytest.mark.asyncio
async def test_delete_booking(booking_service):
	user_id = "5973c285-25c7-418a-a521-dc202023ca34"
	request:BookingCreate=BookingCreate(
			name="John Doe",
			restaurant_id="c32b9038-24f4-4d2d-8e9b-8c1b67531c95",
			email="john.doe@example.com",
			phone="+1234567890",
			reservation_time=datetime.fromisoformat("2025-12-01T19:30:00+00:00"),
			num_of_guests=4,
			note="Window table, please")
	#1. Create a sample booking
	booking = await booking_service.create_booking_order(user_id=user_id,request=request)
	#2. The booking is accepted
	await booking_service.accept_booking_order(booking_id=booking.booking_id)
	with pytest.raises(DeleteBookingError) as error_type:
		await booking_service.delete_booking(user_id=user_id, booking_id=booking.booking_id)

	# Optional: assert inheritance behavior
	assert isinstance(error_type.value, BookingError)
	assert isinstance(error_type.value, DeleteBookingError)

#2. Accept the booking

