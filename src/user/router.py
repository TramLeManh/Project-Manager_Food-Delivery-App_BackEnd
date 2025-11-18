import uuid

from fastapi import Depends, APIRouter
from starlette import status

from src.auth.dependencies import get_current_user_id
from src.core.models_response import success
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
