import logging
import uuid

from lxml.parser import result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.entity import UserEntity
from user.exception import UserAlreadyExistsError, UserUpdateError
from user.mapper import user_entity_to_model
from user.model import UserCreate, UserUpdate, UserResponse
from user.repository import UserRepository
from user.utils import hash_password


class UserService:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_user(self, user: UserCreate) -> UserEntity:
		try:
			repository = UserRepository(self.session)
			if await repository.is_email_exist(str(user.email)):
				raise UserAlreadyExistsError("Email already exists")
			hashed_password = hash_password(user.password)
			user_entity = UserEntity(
				user_id=uuid.uuid4(),
				email=str(user.email),
				password=hashed_password,
				address=str(user.address),
				mobile_number=str(user.mobile_number),
			)
			await repository.create_user(user_entity)
			return user_entity
		except IntegrityError:
			await self.session.rollback()
			raise UserAlreadyExistsError("User already exists")
		except Exception as e:
			await self.session.rollback()
			logging.error(e)
			raise

	async def update_user(self, user_id: uuid.uuid4(), user: UserUpdate) -> UserResponse:
		try:
			repository = UserRepository(self.session)
			if await repository.is_email_exist(str(user.email)):
				raise UserAlreadyExistsError("Email already exists")
			hashed_password = hash_password(user.password)
			user_entity = UserEntity(
				user_id=user_id,
				email=str(user.email),
				password=hashed_password,
				address=str(user.address),
				mobile_number=str(user.mobile_number),
			)

			result = await repository.update_user(user_id=user_id, updates=user_entity)
			if result is None:
				raise UserUpdateError()
			user_response = user_entity_to_model(result)

			return user_response
		except IntegrityError:
			await self.session.rollback()
			raise UserAlreadyExistsError("User already exists")
		except Exception as e:
			await self.session.rollback()
			logging.error(e)
			raise

	async def get_user_profile(self, user_id: str) -> UserResponse:
		repository = UserRepository(self.session)
		user = await repository.get_user_by_id(user_id)

		return user_entity_to_model(user)
