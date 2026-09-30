
from starlette import status

from src.core.exceptions import BaseError


class BookingError(BaseError):
	pass


class  BookingNotFoundError(BookingError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Can not find booking"
		super().__init__(message=message, code=-1, status_code=status_code)
class  UpdateBookingError(BookingError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Can not find booking"
		super().__init__(message=message, code=-1, status_code=status_code)
class  AcceptBookingError(BookingError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Can not accept booking"
		super().__init__(message=message, code=-1, status_code=status_code)
class  DeleteBookingError(BookingError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Can not delete booking"
		super().__init__(message=message, code=-1, status_code=status_code)
class  RejectBookingError(BookingError):
	def __init__(self):
		status_code = status.HTTP_400_BAD_REQUEST
		message = "Can not reject the booking"
		super().__init__(message=message, code=-1, status_code=status_code)