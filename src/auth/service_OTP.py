import json
from datetime import datetime, timedelta, timezone
from typing import Optional

from redis import Redis

from src.auth.exception import OTPError, InvalidOTPError, ExpireOTPError
from src.core.config import settings
from src.core.utils import generate_session_id


class OTPService:
	def __init__(self, redis_client: Redis):
		self.redis = redis_client

	def store_otp(self, email: str, otp: str) -> str:
		"""
		Store OTP in Redis with session ID
		Returns: (session_id, expiry_datetime)
		"""
		session_id = generate_session_id()
		expiry_time = timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
		expires_at = datetime.now(timezone.utc) + expiry_time

		# 1. Store OTP data as JSON
		otp_data = {
			"email": email,
			"otp": otp,
			"created_at": datetime.now(timezone.utc).isoformat(),
			"expires_at": expires_at.isoformat(),
			"verified": False
		}

		# 2. Store in Redis with expiry
		key = f"otp:{session_id}"
		self.redis.setex(
			key,
			expiry_time,
			json.dumps(otp_data)
		)

		return session_id

	def invalidate_session(self, session_id):
		"""Delete session from Redis"""
		key = f"otp:{session_id}"
		self.redis.delete(key)

	def verify_otp(self, session_id: str, otp: str) -> tuple[bool, Optional[str]]:
		"""
				Verify OTP for a given session
				Returns: (is_valid, email)
				"""
		key = f"otp:{session_id}"

		# 1. Get OTP data from Redis
		otp_data_str = self.redis.get(key)
		if not otp_data_str:
			raise ExpireOTPError()

		otp_data = json.loads(otp_data_str)

		# 2. Check if already verified
		if otp_data.get("verified"):
			raise InvalidOTPError()

		# 3. Verify OTP
		if otp_data["otp"] != otp:
			raise InvalidOTPError()
		otp_data["verified"] = True
		otp_data["verified_at"] = datetime.now(timezone.utc).isoformat()

		# Update in Redis with extended expiry for password reset
		session_expiry = timedelta(minutes=settings.SESSION_EXPIRY_MINUTES)
		self.redis.setex(
			key,
			session_expiry,
			json.dumps(otp_data)
		)
		return otp_data["email"]

	def get_session_data(self, session_id: str) -> Optional[dict]:
		try:
			"""Get session data from Redis"""
			key = f"otp:{session_id}"
			otp_data_str = self.redis.get(key)

			if not otp_data_str:
				raise ExpireOTPError()

			return json.loads(otp_data_str)
		except OTPError:
			raise
		except Exception:
			raise
