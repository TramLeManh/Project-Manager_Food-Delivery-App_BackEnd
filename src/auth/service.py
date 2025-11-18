import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exception import InvalidUsernamePassword, TokenError
from src.auth.utils import create_access_token
from src.user.repository import UserRepository
from src.user.utils import verify_password


class AuthService:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def authenticate_user(self, email: str, password: str) -> str:
		try:
			# 1. Find user from db
			repository = UserRepository(self.session)
			user = await repository.get_user_by_mail(email)
			if user is None:
				raise InvalidUsernamePassword()
			# NOte khi nhan id type UUID thì chuyển sang UUID
			user_id = str(user.user_id)
			# 2. Verify password
			if verify_password(plain_password=password, hashed_password=user.password) is False:
				raise InvalidUsernamePassword()
			# Check active user:
			# 3. Generate access token
			access_token = create_access_token(data={"id": user_id})

			return access_token
		except TokenError as e:
			raise
		except Exception as e:
			await self.session.rollback()
			logging.error(e)
