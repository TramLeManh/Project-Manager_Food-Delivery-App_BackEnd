from fastapi import APIRouter, Depends, Query

from src.auth.dependencies import get_current_user_id
from src.core.models_response import success
from src.order.dependencies import get_booking_service
from src.order.entity import BookingStatus
from src.order.model import Booking
from src.order.service import BookingService
from src.restaurant.dependencies import get_restaurant_service
from src.restaurant.model import RestaurantCreate, RestaurantModel
from src.restaurant.service import RestaurantService

router = APIRouter()


@router.get("/restaurant/{restaurant_id}/booking", response_model=list[Booking])
async def list_restaurants(
		restaurant_id: str,
		booking_service: BookingService = Depends(get_booking_service),
		booking_status: int = Query(None),
		# user_id=Depends(get_current_user_id)
):
	status = None
	if booking_status:
		status = BookingStatus.from_int(booking_status)
	data = await booking_service.get_list_booking_order_by_restaurant_id(restaurant_id=restaurant_id,
	                                                                     booking_status=status)
	return success(data=data)


@router.post("/booking/{booking_id}/accept", response_model=list[Booking])
async def list_restaurants(
		booking_id: str,
		booking_service: BookingService = Depends(get_booking_service),

		# user_id=Depends(get_current_user_id)
):
	data = await booking_service.accept_booking_order(booking_id=booking_id)
	message = f"Booking {booking_id} has been accepted"

	return success(data=data, message=message)


@router.post("/booking/{booking_id}/reject", response_model=list[Booking])
async def list_restaurants(
		booking_id: str,
		booking_service: BookingService = Depends(get_booking_service),
		# user_id=Depends(get_current_user_id)
):
	await booking_service.reject_booking_order(booking_id=booking_id)
	message = f"Booking {booking_id} has been rejected"
	return success(message=message)


@router.post("/restaurant/create")
async def list_restaurants(
		data: RestaurantCreate,
		restaurant_service: RestaurantService = Depends(get_restaurant_service),
		user_id=Depends(get_current_user_id),
):
	await restaurant_service.create_restaurant(owner_id=user_id, request=data)
	message = "Created restaurant success"
	return success(message=message)


@router.put("/restaurant/{restaurant_id}")
async def list_restaurants(
		restaurant_id: str,
		data: RestaurantCreate,
		restaurant_service: RestaurantService = Depends(get_restaurant_service),
		user_id=Depends(get_current_user_id),
):
	await restaurant_service.update_restaurant(owner_id=user_id, restaurant_id=restaurant_id, request=data)
	message = "Update restaurant success"
	return success(message=message)


@router.delete("/restaurant/{restaurant_id}")
async def delete_restaurant(
		restaurant_id: str,
		data: RestaurantCreate,
		restaurant_service: RestaurantService = Depends(get_restaurant_service),
		user_id=Depends(get_current_user_id),
):
	await restaurant_service.delete_restaurant(owner_id=user_id, restaurant_id=restaurant_id)
	message = "Delete restaurant success"
	return success(message=message)
@router.get("/restaurants", response_model=list[RestaurantModel])
async def list_restaurants(
		restaurant_service: RestaurantService = Depends(get_restaurant_service),
		user_id=Depends(get_current_user_id)
):

	data:list[RestaurantModel] = await restaurant_service.get_admin_restaurants(admin_id=user_id)
	return success(data=data)