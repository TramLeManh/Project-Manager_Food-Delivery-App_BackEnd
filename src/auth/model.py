from datetime import datetime
from typing import Optional

from anthropic import BaseModel
from pydantic import EmailStr, Field


class Token(BaseModel):
	access_token: str
	role:str
	model_config = {
			"json_schema_extra": {
				"example": {
					"access_token": "12345678",
					"role": "ADMIN"
				}
			}
		}

class OTPRequest(BaseModel):
	email: EmailStr


class OTPVerify(BaseModel):
	session_id: str
	otp: str


class PasswordReset(BaseModel):
	session_id: str
	password: str = Field(..., min_length=8, description="New password must be at least 8 characters")


class OTPResponse(BaseModel):
	session_id: Optional[str] = None
