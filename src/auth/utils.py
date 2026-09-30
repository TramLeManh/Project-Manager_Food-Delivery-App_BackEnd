import logging
import random
import string
from datetime import datetime, timedelta, timezone

from authlib.jose import jwt

from src.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode({'alg': settings.JWT_ALGORITHM}, to_encode, settings.JWT_SECRET_KEY)
	return encoded_jwt


def generate_otp():
	return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))


def verify_token(token: str):
	try:
		payload = jwt.decode(token, settings.JWT_SECRET_KEY)
		user_id: str = payload.get("user_id")
		if user_id is None:
			return None
		return user_id
	except Exception as e:
		logging.error(e)
		return None
