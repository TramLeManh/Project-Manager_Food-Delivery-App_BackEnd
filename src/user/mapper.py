from src.user.entity import UserEntity
from src.user.model import UserResponse, UserRole


def user_entity_to_model(user: UserEntity) -> UserResponse:
	is_admin = user.role == UserRole.ADMIN
	user_response = UserResponse(email=user.email, id=user.user_id, phone_number=user.mobile_number,
	                             address=user.address, isAdmin=is_admin)
	return user_response.model_dump(exclude_none=True, by_alias=True)
