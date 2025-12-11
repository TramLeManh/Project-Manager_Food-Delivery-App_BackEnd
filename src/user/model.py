import uuid
from enum import Enum as PyEnum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBase(BaseModel):
	email: EmailStr
	# 1. Alias dùng trong payload trả cho FE. Take out key từ mongo. Param của model. phoneNumber là param trong json ?
	phone_number: Optional[str] = Field(None, alias="phone_number")

	address: Optional[str]

	model_config = {
		"populate_by_name": False
	}


class UserUpdate(BaseModel):
	email: EmailStr
	phone_number: Optional[str]
	address: Optional[str]
	password: str


class UserRole(str, PyEnum):
	USER = "USER"
	ADMIN = "ADMIN"


class UserCreate(UserBase):
	password: str
	isAdmin: Optional[bool] = False



	model_config = {
		"json_schema_extra": {
			"example": {
				"email": "kareno1412@gmail.com",
				"phone_number": "+1234567890",
				"address": "123 Example Street, City",
				"password": "12345678",
				"isAdmin": True,
			}

		}
	}


class UserResponse(UserBase):
	id: str
	isAdmin: bool

	@field_validator("id", mode="before")
	def convert_uuid_to_str(cls, v):
		if isinstance(v, uuid.UUID):
			return str(v)
		return v

	model_config = {
		"populate_by_name": False,
		"from_attributes": True
	}
