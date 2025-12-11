import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exception import InvalidUsernamePassword, TokenError, OTPError, NotVerifiedError
from src.auth.model import OTPResponse, Token
from src.auth.service_OTP import OTPService
from src.auth.service_email import EmailService
from src.auth.utils import create_access_token, generate_otp
from src.core.utils import hash_password, verify_password
from src.user.exception import UserError
from src.user.exception import UserNotFoundError
from src.user.repository import UserRepository


class AuthService:
	def __init__(self, session: AsyncSession, otp_service: OTPService, email_service: EmailService):
		self._tasks = []
		self.session = session
		self.otp_service = otp_service
		self.email_service = email_service

	async def authenticate_user(self, email: str, password: str) -> Token:
		try:
			# 1. Find user from db
			repository = UserRepository(self.session)
			user = await repository.get_user_by_mail(email)
			if user is None:
				raise InvalidUsernamePassword()
			# NOte khi nhan id type UUID thì chuyển sang UUID
			user_id = str(user.user_id)
			# 2. Verify password
			if not verify_password(plain_password=password, hashed_password=user.password):
				raise InvalidUsernamePassword()
			# Check active user:
			# 3. Generate access token
			access_token = create_access_token(data={"id": user_id})
			user_role: str = user.role.value
			token: Token = Token(access_token=access_token, role=user_role)
			return token
		except TokenError as e:
			raise
		except Exception as e:
			await self.session.rollback()
			logging.error(e)

	async def request_otp(self, email: str) -> OTPResponse:
		try:
			# 1. Check if user's email exist:
			user_repository = UserRepository(self.session)
			is_user_exists = await user_repository.is_email_exist(email=email)
			if not is_user_exists:
				raise UserNotFoundError()
			# 2. Generate OTP
			otp = generate_otp()
			session_id = self.otp_service.store_otp(email, otp)
			task = asyncio.create_task(
				self.email_service.send_otp_email(email, otp)

			)
			self._tasks.append(task)
			task.add_done_callback(self._tasks.remove)
			return OTPResponse(session_id=session_id)

		except UserError:
			raise

	async def reset_password(self, session_id: str, new_password: str):
		try:
			user_repository = UserRepository(self.session)
			session_data = self.otp_service.get_session_data(session_id)
			if not session_data.get("verified"):
				raise NotVerifiedError()
			email = session_data["email"]
			hashed_password = hash_password(new_password)
			await user_repository.update_password(email, hashed_password)
			self.otp_service.invalidate_session(session_id)
			return True
		except OTPError:
			raise
		except Exception:
			raise

	def verify_otp(self, session_id: str, otp: str) -> bool:
		try:
			self.otp_service.verify_otp(session_id, otp)
			return True
		except OTPError as e:
			raise e
		except Exception:
			raise
