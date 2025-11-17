from starlette import status

from src.core.exceptions import BaseError


class UserError(BaseError):
	pass


class UserNotFoundError(UserError):
	def __init__(self):
		status_code = status.HTTP_404_NOT_FOUND
		message = "User not found"
		super().__init__(message=message, code=-1, status_code=status_code)


class UserAlreadyExistsError(UserError):
	def __init__(self, message):
		status_code = status.HTTP_400_BAD_REQUEST
		super().__init__(message=message, code=-1, status_code=status_code)


class UserUpdateError(UserError):
	def __init__(self):
		message = "User update failed"
		status_code = status.HTTP_400_BAD_REQUEST
		super().__init__(message=message, code=-1, status_code=status_code)
