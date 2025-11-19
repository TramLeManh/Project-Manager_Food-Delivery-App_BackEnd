import uuid

from sqlalchemy import select, exists, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.entity import UserEntity


class UserRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def is_email_exist(self, email: str) -> bool:
		stmt = select(exists().where(UserEntity.email == email))
		result = await self.session.execute(stmt)
		return result.scalar()

	async def get_user_by_mail(self, user_email: str) -> UserEntity:
		stmt = select(UserEntity).filter(UserEntity.email == user_email)
		result = await self.session.execute(stmt)
		user_entity = result.scalar_one_or_none()
		return user_entity

	async def get_user_by_id(self, user_id: uuid.UUID) -> UserEntity:
		stmt = select(UserEntity).filter(UserEntity.user_id == user_id)
		result = await self.session.execute(stmt)
		user_entity = result.scalar_one_or_none()
		return user_entity

	async def create_user(self, user: UserEntity) -> uuid.UUID:
		self.session.add(user)
		await self.session.flush()
		return user.user_id

	async def update_user(self, user_id: uuid.UUID, updates: UserEntity) -> UserEntity | None:
		stmt = select(UserEntity).filter_by(user_id=user_id)
		result = await self.session.execute(stmt)
		existing_user = result.scalar_one_or_none()
		if existing_user is None:
			return None

		mapper = inspect(UserEntity).mapper

		for attr in mapper.column_attrs:
			key = attr.key
			if key == "user_id":
				continue

			value = getattr(updates, key)
			setattr(existing_user, key, value)

		await self.session.commit()
		return existing_user

	async def update_password(self, email: str, new_hashed_password: str) -> bool:
		stmt = select(UserEntity).filter_by(email=email)
		result = await self.session.execute(stmt)
		user = result.scalar_one_or_none()
		if user is None:
			return False

		user.password = new_hashed_password  # Assuming `password` is a column in `UserEntity`
		await self.session.commit()
		return True
