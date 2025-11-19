from authlib.jose import jwt, JoseError
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exception import InvalidCredentialsError
from src.auth.service_auth import AuthService
from src.auth.service_OTP import OTPService
from src.core.config import settings
from src.core.dependencies import get_session, get_redis_client

security = HTTPBearer()


def get_auth_service(session: AsyncSession = Depends(get_session), redis_client=Depends(get_redis_client)
                     ) -> AuthService:
	otp_service = OTPService(redis_client=redis_client)
	from src.auth.service_email import EmailService
	email_service = EmailService()
	return AuthService(session=session, otp_service=otp_service,email_service=email_service)


async def get_current_user_id(
		credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
	token = credentials.credentials
	try:
		payload = jwt.decode(token, settings.JWT_SECRET_KEY)
		_user_id: str = payload.get("id")
		if _user_id is None:
			raise InvalidCredentialsError()

		return _user_id
	except JoseError:
		raise
