from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from src.core.config import settings
from authlib.jose import jwt
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode({'alg': settings.JWT_ALGORITHM}, to_encode, settings.JWT_SECRET_KEY)
	return encoded_jwt


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