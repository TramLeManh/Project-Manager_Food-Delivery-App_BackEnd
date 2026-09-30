import asyncio
import logging
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service_email import EmailService
from src.core.utils import hash_password
from src.user.entity import UserEntity
from src.user.exception import EmailExistsError, UserUpdateError
from src.user.mapper import user_entity_to_model
from src.user.model import UserCreate, UserResponse, UserUpdate, UserRole
from src.user.repository import UserRepository
from src.user.utils import EmailConstraint


class UserService:
	def __init__(self, session: AsyncSession, email_service: EmailService):
		self.session = session
		self.email_service = email_service
		self._tasks = []

	async def create_user(self, user: UserCreate) -> UserEntity:
		try:
			repository = UserRepository(self.session)
			hashed_password = hash_password(user.password)
			user_entity = UserEntity(
				user_id=uuid.uuid4(),
				email=str(user.email),
				password=hashed_password,
				address=str(user.address),
				mobile_number=str(user.phone_number),
			)
			if user.isAdmin:
				user_entity.role = UserRole.ADMIN
			await repository.create_user(user_entity)
			task = asyncio.create_task(
				self.email_service.send_welcome_email(user_entity.email, user_entity.email)

			)
			self._tasks.append(task)
			task.add_done_callback(self._tasks.remove)
			return user_entity
		except IntegrityError as e:
			exception_response = e.args[0]
			if EmailConstraint in exception_response:
				raise EmailExistsError()
		except Exception as e:
			await self.session.rollback()
			logging.error(e)
			raise

	async def update_user(self, user_id: uuid.uuid4(), user: UserUpdate) -> UserResponse | None:
		try:
			repository = UserRepository(self.session)
			hashed_password = hash_password(user.password)
			user_entity = UserEntity(
				user_id=user_id,
				email=str(user.email),
				password=hashed_password,
				address=str(user.address),
				mobile_number=str(user.phone_number),
			)

			result = await repository.update_user(user_id=user_id, updates=user_entity)
			if result is None:
				raise UserUpdateError()
			user_response = user_entity_to_model(result)

			return user_response
		except IntegrityError as e:
			exception_response = e.args[0]
			if EmailConstraint in exception_response:
				raise EmailExistsError()
		except Exception as e:
			await self.session.rollback()
			logging.error(e)
			raise

	async def get_user_profile(self, user_id: uuid.UUID) -> UserResponse:
		repository = UserRepository(self.session)
		user = await repository.get_user_by_id(user_id)
		return user_entity_to_model(user)
