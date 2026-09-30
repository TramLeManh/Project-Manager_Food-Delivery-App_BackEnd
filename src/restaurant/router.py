from fastapi import APIRouter, Depends, Query

from src.auth.dependencies import get_current_user_id
from src.core.models_response import success
from src.restaurant.dependencies import get_restaurant_service
from src.restaurant.model import RestaurantModel, RestaurantFilter, RestaurantCreate
from src.restaurant.service import RestaurantService

router = APIRouter()


@router.get("/", response_model=list[RestaurantModel])
async def list_restaurants(
		restaurant_service: RestaurantService = Depends(get_restaurant_service),
		district: str | None = Query(None, description="Filter by district UUID"),
		category: str | None = Query(None, description="Filter by category UUID"),
):
	request = RestaurantFilter(district=district, category=category)
	data = await restaurant_service.get_restaurants(request)
	return success(data=data)
router.redirect_slashes = False

@router.get("/{restaurant_id}", response_model=list[RestaurantModel])
async def list_restaurants(restaurant_id: str, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
	data = await restaurant_service.get_restaurant_by_id(restaurant_id)
	return success(data=data)



