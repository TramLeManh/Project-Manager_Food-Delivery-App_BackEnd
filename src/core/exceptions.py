import logging

from authlib.common.errors import AuthlibBaseError
from fastapi import HTTPException, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.core.models_response import server_error, invalid_request, invalid_token


class BaseError(HTTPException):

	def __init__(self, *, status_code: int | None = None, code: int | None = None, message: str | None = None):
		super().__init__(status_code=status_code or 200, detail=message)
		self.code = code or 0
		self.message = message


async def unhandled_handler(request: Request, exc: Exception):
	"""Handle unexpected exceptions (not explicitly caught)."""
	logging.exception(f"Unhandled exception: {exc.__class__.__name__}")
	return server_error(message="Internal server error")


async def base_error_handler(request: Request, exc: BaseError):
	response = {"code": exc.code}
	status_code = exc.status_code or 200
	if exc.message:
		response["message"] = exc.message
	return JSONResponse(status_code=status_code, content=response)


async def invalid_token_handler(request: Request, exc: AuthlibBaseError):
	return invalid_token(status_code=401)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
	"""Handle Pydantic validation errors."""
	logging.exception(f"Validation exception: {exc.args[0]}")
	return invalid_request()


async def value_error_handler(request: Request, exc: ValueError):
	"""Handle Pydantic validation errors."""
	logging.exception(f"Validation exception: {exc}")
	message = "Value error"
	return invalid_request(message=message)


def setup_exception_handlers(app: FastAPI):
	"""
	Register all global exception handlers.
	Call this in src/main.py after creating FastAPI app.
	"""
	app.add_exception_handler(AuthlibBaseError, invalid_token_handler)
	app.add_exception_handler(Exception, unhandled_handler)
	app.add_exception_handler(BaseError, base_error_handler)
	app.add_exception_handler(RequestValidationError, validation_exception_handler)
	app.add_exception_handler(ValueError, value_error_handler)
