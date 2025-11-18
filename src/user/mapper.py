from src.user.entity import UserEntity
from src.user.model import UserResponse


def user_entity_to_model(user: UserEntity) -> UserResponse:
	user_response = UserResponse(email=user.email, id=user.user_id, mobile_number=user.mobile_number,
	                             address=user.address)
	return user_response.model_dump(exclude_none=True)
