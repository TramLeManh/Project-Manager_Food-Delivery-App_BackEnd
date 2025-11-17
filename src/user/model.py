import uuid
from typing import Optional

from pydantic import EmailStr, BaseModel, field_validator


class UserBase(BaseModel):
	email: EmailStr
	mobile_number: Optional[str]
	address: Optional[str]


class UserUpdate(BaseModel):
	email: EmailStr
	mobile_number: Optional[str]
	address: Optional[str]
	password: str


class UserCreate(UserBase):
	password: str


class UserResponse(UserBase):
	id: str

	@field_validator("id", mode="before")
	def convert_uuid_to_str(cls, v):
		if isinstance(v, uuid.UUID):
			return str(v)
		return v

	class Config:
		from_attributes = True
