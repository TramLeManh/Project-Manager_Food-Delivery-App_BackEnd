import uuid

from sqlalchemy import Column, UUID, String, DateTime, func

from src.core.entity.Base import Base


class UserEntity(Base):
	__tablename__ = 'user'

	# Tương ứng với: user_id UUID PRIMARY KEY
	user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

	email = Column(String(50), unique=True, nullable=False)
	mobile_number = Column(String(15), nullable=False)
	address = Column(String(50), nullable=False)
	password = Column(String(100), nullable=False)
	# Tương ứng với: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

	def __repr__(self):
		return f"<User(user_id={self.user_id}, email='{self.email}', email='{self.email}')>"
