from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# Security
	JWT_SECRET_KEY: str = "um@a+2j56#xh$r7j*600$#go9&spk5&kxd@y1p-ozi^q#08+hzsvpbrd6iunih++$k=(nq#f"
	JWT_ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	# OTP
	OTP_LENGTH: int = 5
	OTP_EXPIRY_MINUTES: int = 10
	SESSION_EXPIRY_MINUTES: int = 30
	# CORS
	ALLOWED_HOSTS: List[str] = ["*"]

	# Pagination
	DEFAULT_PAGE_SIZE: int = 20
	MAX_PAGE_SIZE: int = 100
	# MongoDB
	MONGO_DATABASE: str = "pm_project"
	MONGO_USERNAME: str = ""
	MONGO_PASSWORD: str = ""
	MONGO_HOSTNAME: str = ""  # The address of your MongoDB server
	MONGO_PORT: int = 27017
	MONGO_URI: str = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"
	# POSTGRES_CONNECTION_STRING
	POSTGRES_USERNAME: str = ""
	POSTGRES_PASSWORD: str = ""
	POSTGRES_HOSTNAME: str = ""
	POSTGRES_PORT: int = 5433
	POSTGRES_DATABASE: str = ""
	POSTGRES_TEST_DATABASE: str = ""
	POSTGRES_BASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}"
	POSTGRES_CONNECTION_URL: str = f"{POSTGRES_BASE_URL}/{POSTGRES_DATABASE}"
	# Redis
	REDIS_HOST: str = ""
	REDIS_USERNAME: str = ""
	REDIS_PASSWORD: str = ""
	REDIS_PORT: int = 6379
	REDIS_DATABASE: int = 0
	#SMTP
	SMTP_HOST:str=""
	SMTP_PORT:str=""
	SMTP_USER:str=""
	SMTP_PASSWORD:str=""
	EMAIL_FROM:str=""
	EMAIL_FROM_NAME:str="support"
	class Config:
		env_file = ".env"
		extra = "allow"  # Allow field that are not defined in model


settings = Settings()
