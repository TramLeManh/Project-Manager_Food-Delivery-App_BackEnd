from authlib.jose import jwt, JoseError
from fastapi import Depends, security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exception import InvalidCredentialsError
from src.auth.service import AuthService
from src.core.config import settings
from src.core.dependencies import get_session
from src.user.exception import UserNotFoundError

security = HTTPBearer()
def get_auth_service(session: AsyncSession = Depends(get_session)
                     ) -> AuthService:
	return AuthService(session=session)
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