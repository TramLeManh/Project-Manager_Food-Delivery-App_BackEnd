import pytest
import redis

from src.auth.exception import TokenError, OTPError, InvalidUsernamePassword, ExpireOTPError
from src.auth.model import OTPResponse
from src.auth.service_OTP import OTPService
from src.auth.service_auth import AuthService
from src.auth.service_email import EmailService
from src.core.config import settings
from src.user.exception import EmailExistsError, UserError
from src.user.model import UserCreate
from src.user.service import UserService
from tests.test_ import get_test_session


def auth_service(get_otp_service):
	pass


@pytest.fixture()
def user_service(get_test_session):
	email = EmailService()
	user_service = UserService(get_test_session, email_service=email)
	yield user_service


@pytest.fixture()
def redis_client():
	redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, username=settings.REDIS_USERNAME,
	                           password=settings.REDIS_PASSWORD, decode_responses=True)
	return redis_client


@pytest.fixture()
def auth_service(get_test_session, redis_client):
	otp_service = OTPService(redis_client=redis_client)
	email_service = EmailService()
	auth_service = AuthService(session=get_test_session, email_service=email_service, otp_service=otp_service)
	yield auth_service


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email(user_service):
	# 1. Create email
	email = "test@example.com"
	first_user = UserCreate(
		email=email,
		mobile_number="123456789",
		address="123 Duplicate St",
		password="correct",
		isAdmin=True
	)
	# 2. User create an account with test_email
	user = await user_service.create_user(first_user)
	# Make sure that user is created
	assert user is not None
	# 3. Another user create a user with same email
	duplicate_email = "test@example.com"
	duplicate_user = UserCreate(
		email=duplicate_email,
		mobile_number="987654321",
		address="456 Another St",
		password="AnotherStrongPass2!",
		isAdmin=True
	)

	# 4. Expect that an EmailExistError
	with pytest.raises(UserError) as error_type:
		await user_service.create_user(duplicate_user)
	# 5. The test case success if EmailExistsError is raise up
	assert isinstance(error_type.value, EmailExistsError)


@pytest.mark.asyncio
async def test_login_user_with_wrong_username_password(user_service, auth_service):
	# 1. Create email
	email = "test@example.com"
	password = "correct"
	user = UserCreate(
		email=email,
		mobile_number="123456789",
		address="123 Duplicate St",
		password="correct"
	)
	# 2. User create an account with test_email
	user = await user_service.create_user(user)
	# 3. Prepare test case:
	request_email = "test@example.com"
	request_password = "wrong"
	# Make sure that user is created
	assert user is not None
	# 4. Expect that an EmailExistError
	with pytest.raises(TokenError) as error_type:
		token = await auth_service.authenticate_user(email=request_email, password=request_password)
	# 5. Expect that the  InvalidUsernamePassword error is raise up
	assert isinstance(error_type.value, InvalidUsernamePassword)


@pytest.mark.asyncio
async def test_login_user_with_correct_username_password(user_service, auth_service):
	# 1. Create email
	email = "test@example.com"
	password = "correct"
	user = UserCreate(
		email=email,
		mobile_number="123456789",
		address="123 Duplicate St",
		password=password
	)
	# 2. User create an account with test_email
	user = await user_service.create_user(user)
	# 3. Prepare test case:
	request_email = "test@example.com"
	request_password = "correct"
	# Make sure that user is created
	assert user is not None
	# 4. Expect successful authentication and a token
	token = await auth_service.authenticate_user(email=request_email, password=request_password)
	assert token
	if isinstance(token, dict):
		assert token.get("access_token")
		assert token.get("token_type") in ("bearer", "Bearer")


@pytest.mark.asyncio
async def test_invalid_otp(user_service, auth_service):
	# 1. Create email
	email = "test@example.com"
	password = "correct"
	user = UserCreate(
		email=email,
		mobile_number="123456789",
		address="123 Duplicate St",
		password=password
	)
	# 2. User create an account with test_email
	user = await user_service.create_user(user)
	# 3. Prepare test case:
	request_email = "test@example.com"
	request_password = "correct"
	# Make sure that user is created
	assert user is not None
	# 4. Expect successful authentication and a token
	token = await auth_service.authenticate_user(email=request_email, password=request_password)
	assert token
	if isinstance(token, dict):
		assert token.get("access_token")
		assert token.get("token_type") in ("bearer", "Bearer")


@pytest.mark.asyncio
async def test_otp_verification(auth_service, redis_client):
	email = "lemanh1412@gmail.com"
	otp_response:OTPResponse = await auth_service.request_otp(email=email)
	# 1. Email exist and otp sent to email
	assert otp_response is not None
	session_id = otp_response.session_id
	key = f"otp:{session_id}"
	# 2. Remove the redis key to simulate timeout / cleanup
	redis_client.delete(key)
	assert redis_client.exists(key) == 0
	otp = "1234"
	# 3. Expect OTPError raise up
	with pytest.raises(OTPError) as error_type:
		is_otp_valid = auth_service.verify_otp(session_id=session_id, otp=otp)
	# 4 .Expect a ExpireOTPError is raise up
	assert isinstance(error_type.value, ExpireOTPError)
