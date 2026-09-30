from typing import Optional

from pydantic import BaseModel


class Booking(BaseModel):
	user_id: Optional[str] = None
	booking_id: Optional[str] = None
	restaurant_image: Optional[str] = None
	name: str
	restaurant_id: str
	booking_status: Optional[str] = None
	email: str
	phone: str
	reservation_time: str
	num_of_guests: int
	note: str

	model_config = {
		"json_schema_extra": {
			"example": {
				"user_id": "5973c285-25c7-418a-a521-dc202023ca34",
				"booking_id": "b456",
				"name": "Manh",
				"restaurant_id": "c32b9038-24f4-4d2d-8e9b-8c1b67531c95",
				"booking_status": "confirmed",
				"email": "lemanh1412@gmail.com",
				"phone": "09196114612",
				"reservation_time": "2025-12-04T06:00:00Z",
				"num_of_guests": 4,
				"note": "Table by the window"
			}
		}
	}

class UpdateBooking(BaseModel):
	customer_name: str
	email: str
	phone: str
	reservation_time: str
	num_of_guests: int
	note: Optional[str]

class BookingCreate(BaseModel):
	name: str
	restaurant_id: str
	email: str
	phone: str
	reservation_time: str
	num_of_guests: int
	note: str

	model_config = {
		"json_schema_extra": {
			"example": {
				"name": "Manh",
				"restaurant_id": "c32b9038-24f4-4d2d-8e9b-8c1b67531c95",
				"email": "lemanh1412@gmail.com",
				"phone": "0919611612",
				"reservation_time": "2025-12-04T06:00:00Z",
				"num_of_guests": 4,
				"note": "Table by the window"
			}
		}
	}
