from starlette import status

from src.core.exceptions import BaseError


# Token Error
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


# OTP error
class OTPError(BaseError):
	pass


class InvalidOTPError(BaseError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Invalid OTP"
		super().__init__(message=message, code=-1, status_code=status_code)


class ExpireOTPError(OTPError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Expire OTP"
		super().__init__(message=message, code=-2, status_code=status_code)


class NotVerifiedError(OTPError):
	def __init__(self):
		status_code = status.HTTP_401_UNAUTHORIZED
		message = "OTP Not Verified"
		super().__init__(message=message, code=-3, status_code=status_code)
