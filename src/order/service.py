import asyncio
from datetime import datetime, timezone

from src.auth.service_email import EmailService
from src.core.utils import generate_uuid
from src.order.entity import BookingEntity, BookingStatus
from src.order.exception import BookingNotFoundError, BookingError, AcceptBookingError, RejectBookingError
from src.order.model import BookingCreate, Booking, UpdateBooking
from src.order.repository import BookingRepository
from src.order.utils import from_entity_to_model
from src.restaurant.repository import RestaurantRepository
from src.user.repository import UserRepository


class BookingService:
	def __init__(self, booking_repository: BookingRepository, restaurant_repository: RestaurantRepository,
	             email_service: EmailService, user_repository: UserRepository):
		self._tasks = []
		self.booking_repository = booking_repository
		self.restaurant_repository = restaurant_repository
		self.email_service = email_service
		self.user_repository = user_repository

	# User
	# 1, Create booking order
	async def create_booking_order(self, user_id: str, request: BookingCreate) -> BookingEntity:
		try:
			booking_id = generate_uuid()
			booking_status: BookingStatus = BookingStatus.PENDING
			restaurant = await self.restaurant_repository.get_restaurant_by_id(request.restaurant_id)
			# Validate restaurant
			booking_entity = BookingEntity(user_id=user_id, restaurant_id=request.restaurant_id,
			                               restaurant_image=restaurant.image,
			                               booking_id=booking_id,
			                               booking_status=booking_status, email=request.email,
			                               phone=request.phone, num_of_guests=request.num_of_guests,
			                               reservation_time=request.reservation_time,
			                               note=request.note, customer_name=request.name)
			await self.booking_repository.create_booking(booking_entity)
			restaurant = await self.restaurant_repository.get_restaurant_by_id(request.restaurant_id)
			admin = await self.user_repository.get_user_by_id(restaurant.owner_id)

			task1 = asyncio.create_task(
				self.email_service.send_pending_email(email=request.email, restaurant_name=restaurant.name,
				                                      booking=booking_entity)

			)

			task2 = asyncio.create_task(
				self.email_service.send_announce_admin(
					admin_email=admin.email, restaurant=restaurant, booking=booking_entity
				)
			)
			self._tasks.append(task1)
			self._tasks.append(task2)

			# CALLBACK XÓA AN TOÀN
			task1.add_done_callback(lambda t: self._safe_remove_task(t))
			task2.add_done_callback(lambda t: self._safe_remove_task(t))
			return booking_entity
		except Exception as e:
			raise

	# 2. Get list of current booking order base on status
	async def get_list_user_booking_orders(self, user_id: str, booking_status: BookingStatus) -> list[Booking]:
		bookings = await self.booking_repository.get_user_booking_by_status(user_id=user_id,
		                                                                    booking_status=booking_status)
		return [from_entity_to_model(booking) for booking in bookings]

	# 3 Get list booking by user_id
	async def get_list_booking_order_by_restaurant_id(self, restaurant_id: str, booking_status: BookingStatus | None):
		bookings = await self.booking_repository.get_user_booking_by_restaurant_id(restaurant_id=restaurant_id,
		                                                                           booking_status=booking_status)
		return [from_entity_to_model(booking) for booking in bookings]

	async def get_detail_booking_order(self, booking_id: str):
		booking = await self.booking_repository.get_booking_by_id(booking_id=booking_id)
		return from_entity_to_model(booking)

	async def delete_booking(self, user_id, booking_id: str) -> bool:
		try:
			booking = await self.booking_repository.get_booking_by_id(booking_id=booking_id)
			if booking is None:
				raise BookingNotFoundError
			booking_status = BookingStatus.from_int(booking.booking_status)
			# if booking_status == BookingStatus.ACCEPTED:
			# # if datetime.now(timezone.utc) < booking.reservation_time:
			# # 	raise DeleteBookingError
			result = await self.booking_repository.delete_booking(user_id=user_id, booking_id=booking_id)
			if result is False:
				raise BookingNotFoundError
			return True
		except BookingError:
			raise
		except Exception:
			raise

	async def accept_booking_order(self, booking_id: str):
		try:
			booking = await self.booking_repository.get_booking_by_id(booking_id=booking_id)
			restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id=booking.restaurant_id)
			if booking is None:
				raise BookingNotFoundError
			booking_status = BookingStatus.from_int(booking.booking_status)
			if booking_status is not BookingStatus.PENDING:
				raise AcceptBookingError
			# if datetime.now(timezone.utc) > booking.reservation_time:
			# 	raise AcceptBookingError
			await self.booking_repository.update_booking_status(booking_id=booking_id,
			                                                    booking_status=BookingStatus.ACCEPTED.get_value())
			task1 = asyncio.create_task(
				self.email_service.send_accept_email(
					email=booking.email, restaurant=restaurant, booking=booking
				),
			)

			self._tasks.extend([task1])
			task1.add_done_callback(self._tasks.remove)
		except BookingError:
			raise
		except Exception:
			raise

	async def reject_booking_order(self, booking_id: str):
		try:
			booking = await self.booking_repository.get_booking_by_id(booking_id=booking_id)
			restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id=booking.restaurant_id)
			if booking is None:
				raise BookingNotFoundError
			booking_status = BookingStatus.from_int(booking.booking_status)
			if booking_status is BookingStatus.ACCEPTED:
				raise RejectBookingError
			# if datetime.now(timezone.utc) > booking.reservation_time:
			# 	raise RejectBookingError
			await self.booking_repository.update_booking_status(booking_id=booking_id,
			                                                    booking_status=BookingStatus.REJECTED.get_value())
			task = asyncio.create_task(
				self.email_service.send_reject_email(email=booking.email, restaurant_name=restaurant.name,
				                                     booking=booking)

			)
			self._tasks.append(task)
			task.add_done_callback(self._tasks.remove)
		except BookingError:
			raise
		except Exception:
			raise

	async def update_booking_order(self, booking_id: str, update_booking: UpdateBooking):
		try:
			booking: BookingEntity = await self.booking_repository.get_booking_by_id(booking_id=booking_id)
			if booking is None:
				raise BookingNotFoundError
			booking_status = BookingStatus.from_int(booking.booking_status)
			if booking_status is not BookingStatus.PENDING:
				raise BookingError(message="Booking status must be PENDING to update.")
			# if datetime.now(timezone.utc) > booking.reservation_time:
			# 	raise BookingError(message="Cannot update booking after the reservation time.")

			# Update booking entity with new fields
			booking.update_from_model(update_booking)
			await self.booking_repository.update_booking(booking)
		except BookingError:
			raise
		except Exception:
			raise

	def _safe_remove_task(self, task):
		try:
			self._tasks.remove(task)
		except ValueError:
			pass
