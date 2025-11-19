import logging

import pytest
import redis

from src.auth.service_auth import AuthService
from src.auth.service_OTP import OTPService
from src.core.config import settings
from tests.test_ import get_real_session


@pytest.fixture()
def auth_service(get_real_session):
	redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, username=settings.REDIS_USERNAME,
	                           password=settings.REDIS_PASSWORD, decode_responses=True)
	logging.basicConfig(
		level=logging.DEBUG,
		format="%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d",
		force=True,
	)
	otp_service = OTPService(redis_client=redis_client)
	service = AuthService(session=get_real_session, otp_service=otp_service)
	yield service


@pytest.mark.asyncio
async def test_request_otp(auth_service):
	email: str = "test@gmail.com"
	response = await auth_service.request_otp(email)
	print(response)


@pytest.mark.asyncio
async def test_verify_otp(auth_service):
	email: str = "test@gmail.com"
	response = auth_service.verify_otp(session_id="4cfccd09-39ae-44f1-bd3c-cb85e8a246fc", otp="33203")
	print(response)


@pytest.mark.asyncio
async def test_reset_password(auth_service):
	session_id: str = "a8d4af96-44b5-4008-8b04-15a3e8af3387"
	password = "12345678"
	response = await auth_service.reset_password(session_id=session_id, new_password=password)
	print(response)
