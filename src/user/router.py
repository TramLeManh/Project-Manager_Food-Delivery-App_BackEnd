import uuid

from fastapi import Depends, APIRouter, Query
from starlette import status

from src.auth.dependencies import get_current_user_id
from src.core.models_response import success
from src.order.dependencies import get_booking_service
from src.order.entity import BookingStatus
from src.order.model import Booking, UpdateBooking, BookingCreate
from src.order.service import BookingService
from src.user.dependencies import get_user_service
from src.user.model import UserResponse, UserCreate, UserUpdate
from src.user.service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
		user_data: UserCreate,
		user_service: UserService = Depends(get_user_service)
):
	await user_service.create_user(user_data)
	message = "Created user successfully"
	return success(message=message)


@router.put("/update", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
		user_data: UserUpdate,
		user_id: uuid.UUID = Depends(get_current_user_id),
		user_service: UserService = Depends(get_user_service)
):
	data = await user_service.update_user(user_id=user_id, user=user_data)
	message = "Update user successfully"
	return success(message=message, data=data)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
		user_id: uuid.UUID = Depends(get_current_user_id),
		user_service: UserService = Depends(get_user_service)
):
	data = await user_service.get_user_profile(user_id=user_id)
	return success(data=data)


@router.get("/booking", response_model=list[Booking])
async def list_restaurants(
		booking_service: BookingService = Depends(get_booking_service),
		booking_status: int | None = Query(None, description="Filter by district UUID"),
		user_id=Depends(get_current_user_id)
):
	status = None
	if booking_status:
		status = BookingStatus.from_int(booking_status)
	data = await booking_service.get_list_user_booking_orders(user_id=user_id, booking_status=status)
	return success(data=data)
@router.get("/booking/{booking_id}")
async def list_restaurants(
		booking_id: str,
		booking_service: BookingService = Depends(get_booking_service),
		user_id=Depends(get_current_user_id),
):
	data = await booking_service.get_detail_booking_order(booking_id=booking_id)
	return success(data=data)

@router.post("/booking")
async def list_restaurants(
		data: BookingCreate,
		booking_service: BookingService = Depends(get_booking_service),
		user_id=Depends(get_current_user_id),
):
	await booking_service.create_booking_order(user_id=user_id, request=data)
	message = "Created booking success"
	return success(message=message)




@router.put("/booking/{booking_id}")
async def list_restaurants(
		data: UpdateBooking,
		booking_id: str,
		booking_service: BookingService = Depends(get_booking_service),
		user_id=Depends(get_current_user_id),
):
	data = await booking_service.update_booking_order(booking_id=booking_id, update_booking=data)
	return success(data=data,message="Update Booking Success")


@router.delete("/booking/{booking_id}")
async def list_restaurants(
		booking_id: str,
		booking_service: BookingService = Depends(get_booking_service),
		user_id=Depends(get_current_user_id)
):
	await booking_service.delete_booking(user_id=user_id, booking_id=booking_id)
	message = "Deleted booking successfully"
	return success(message=message)
