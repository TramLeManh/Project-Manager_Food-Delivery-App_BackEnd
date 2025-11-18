import logging
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from src.user.entity import UserEntity
from src.user.exception import EmailExistsError
from src.user.repository import UserRepository
from src.user.utils import EmailConstraint
from tests.test_ import get_real_session, get_test_session


@pytest.fixture()
def user_repository(get_real_session):
	logging.basicConfig(
		level=logging.DEBUG,
		format="%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d",
		force=True,
	)
	repository = UserRepository(get_real_session)
	yield repository


@pytest.mark.asyncio
async def test_create_user(user_repository):
	try:
		user = UserEntity(
			user_id=uuid.uuid4(),
			email="test@example.com",
		)
		user_id = await user_repository.create_user(user)
		assert user_id == user.user_id
	except IntegrityError as e:
		exception_response = e.args[0]
		if EmailConstraint in exception_response:
			print("Email already exists")
			raise EmailExistsError()


@pytest.mark.asyncio
async def test_retrieves_user_by_id(get_test_session):
	user_repository: UserRepository = UserRepository(get_test_session)
	email = "existing_user@example.com"
	user = UserEntity(
		user_id=uuid.uuid4(),
		email=email,
	)
	await user_repository.create_user(user)
	retrieved_user = await user_repository.get_user_by_mail(email)
	assert retrieved_user == user


@pytest.mark.asyncio
async def test_update_user_email(get_test_session):
	# 1. Assump create a user with old value
	user_repository: UserRepository = UserRepository(get_test_session)
	original_user = UserEntity(user_id=uuid.uuid4(), email="old@gmail.com")
	created_id = await user_repository.create_user(original_user)
	# 2. Update user
	updates = UserEntity(email="new@gmail.com")
	updated = await user_repository.update_user(created_id, updates)
	# 3. Check update result
	assert updated is not None
	assert updated.user_id == created_id
	assert updated.email == "new@gmail.com"
	# 4. Check database again to make sure the data is updated
	fetched = await user_repository.get_user_by_mail(updated.email)
	assert fetched is not None
	assert fetched.email == "new@gmail.com"
