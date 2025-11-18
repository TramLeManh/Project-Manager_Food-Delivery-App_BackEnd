from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.user.service import UserService


def get_user_service(session: AsyncSession = Depends(get_session)):
	return UserService(session)
