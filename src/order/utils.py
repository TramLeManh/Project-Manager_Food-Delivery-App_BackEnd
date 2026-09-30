from src.core.utils import utc_to_local
from src.order.entity import BookingEntity
from src.order.model import Booking

status: dict[int, str] = {
	1: "ACCEPTED",
	-1: "PENDING",
	0: "REJECTED",
}


def from_entity_to_model(entity: BookingEntity) -> Booking:
	time: str = utc_to_local(str(entity.reservation_time))
	return Booking(booking_id=entity.booking_id, restaurant_id=entity.restaurant_id,
	               booking_status=status[entity.booking_status],
	               email=entity.email, phone=entity.phone, note=entity.note, reservation_time=time,
	               num_of_guests=entity.num_of_guests, name=entity.customer_name,
	               restaurant_image=entity.restaurant_image,
	               )
