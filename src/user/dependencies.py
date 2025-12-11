from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.user.service import UserService
from src.auth.service_email import EmailService


def get_user_service(session: AsyncSession = Depends(get_session)):
	email_service = EmailService()
	return UserService(session,email_service=email_service)
