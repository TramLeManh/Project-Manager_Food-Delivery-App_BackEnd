from fastapi import Depends

from src.auth.service_email import EmailService
from src.core.dependencies import get_mongo_db, get_session
from src.order.repository import BookingRepository
from src.order.service import BookingService
from src.restaurant.repository import RestaurantRepository
from src.user.repository import UserRepository


def get_booking_service(database=Depends(get_mongo_db), session=Depends(get_session)):
	booking_repository = BookingRepository(database=database)
	restaurant_repository = RestaurantRepository(database=database)
	user_repository = UserRepository(session=session)

	email_service = EmailService()
	booking_service = BookingService(booking_repository=booking_repository, email_service=email_service,
	                                 restaurant_repository=restaurant_repository, user_repository=user_repository)
	return booking_service
