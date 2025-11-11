from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.core.models.response_model import PaginatedResult


def build_paginated_response(result: PaginatedResult) -> dict:
	return {
		"total": result.total,
		"page": result.page,
		"page_size": result.page_size,
		"data": result.data
	}


class ResponseStatus(int, Enum):
	INVALID_TOKEN = -3
	SUCCESS = 1
	SEVER_ERROR = -1
	FAIL = 0
	BAD_REQUEST = 99
	NOT_FOUND = 4
	INVALID_REQUEST = 5


class APIResponse(BaseModel):
	code: ResponseStatus
	message: Optional[str] = None
	data: Optional[Any] = None


def success(message: Optional[str] = None, data: Any = None) -> JSONResponse:
	response = APIResponse(
		code=ResponseStatus.SUCCESS,
		message=message,
		data=data
	)
	#Not include None in response
	return JSONResponse(status_code=200, content=response.model_dump(exclude_none=True))


def server_error(status_code: Optional[int] = 200, message: Optional[str] = None, data: Any = None) -> JSONResponse:
	response = APIResponse(code=ResponseStatus.SEVER_ERROR, message=message, data=data)
	return JSONResponse(status_code=status_code, content=response.model_dump(exclude_none=True))


def invalid_request(status_code: Optional[int] = 200) -> JSONResponse:
	message = "Invalid request"
	response = APIResponse(code=ResponseStatus.INVALID_REQUEST, message=message)
	return JSONResponse(status_code=status_code, content=response.model_dump(exclude_none=True))
def invalid_token(status_code: Optional[int] = 200) -> JSONResponse:
	message = "Invalid token"
	response = APIResponse(code=ResponseStatus.INVALID_TOKEN, message=message)
	return JSONResponse(status_code=status_code, content=response.model_dump(exclude_none=True))