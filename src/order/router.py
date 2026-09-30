from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user_id
from src.core.models_response import success
from src.order.dependencies import get_booking_service
from src.order.model import BookingCreate
from src.order.service import BookingService

router = APIRouter()




