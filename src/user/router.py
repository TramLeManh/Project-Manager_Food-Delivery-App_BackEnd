from fastapi import Depends, APIRouter
from starlette import status

from src.core.models_response import success
from src.user.dependencies import get_user_service
from src.user.model import UserResponse, UserCreate
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