from datetime import datetime
from enum import Enum

from anthropic import BaseModel

from src.order.model import UpdateBooking


class BookingStatus(int, Enum):
	ACCEPTED = 1
	PENDING = -1
	REJECTED = 0

	@classmethod
	def from_int(cls, value: int) -> "BookingStatus":
		try:
			return cls(value)
		except ValueError:
			raise ValueError(f"Invalid BookingStatus value: {value}")

	def get_value(self) -> int:
		return int(self)


class BookingEntity(BaseModel):
	restaurant_id: str
	restaurant_image: str
	user_id: str
	customer_name: str
	booking_id: str
	booking_status: int
	email: str
	phone: str
	num_of_guests: int
	reservation_time: str
	note: str

	def update_from_model(self, booking_update: UpdateBooking):
		self.customer_name = booking_update.customer_name
		self.email = booking_update.email
		self.phone = booking_update.phone
		self.num_of_guests = booking_update.num_of_guests
		if booking_update.note is not None:
			self.note = booking_update.note
		return self
