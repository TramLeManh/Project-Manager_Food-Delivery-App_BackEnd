from starlette import status

from src.core.exceptions import BaseError


class TokenError(BaseError):
	pass


class InvalidUsernamePassword(TokenError):
	def __init__(self):
		status_code = status.HTTP_401_UNAUTHORIZED
		message = "Invalid username or password"
		super().__init__(message=message, code=-1, status_code=status_code)


class InvalidCredentialsError(TokenError):
	def __init__(self):
		status_code = status.HTTP_401_UNAUTHORIZED
		message = "Invalid token payload"
		super().__init__(message=message, code=-2, status_code=status_code)
