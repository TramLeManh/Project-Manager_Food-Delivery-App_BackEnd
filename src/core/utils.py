import zoneinfo
from datetime import datetime
from uuid import uuid4

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid() -> str:
	return str(uuid4()).split("-")[0]


def generate_session_id() -> str:
	return str(uuid4())


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def utc_to_local(utc_str: str) -> str:
	utc_dt = datetime.fromisoformat(utc_str)
	vn_tz = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")
	local_dt = utc_dt.astimezone(vn_tz)
	return local_dt.strftime("%d-%m-%Y %H:%M:%S")


def iso_to_24h_time(iso_str: str = None) -> str:
	"""
	Convert an ISO datetime string to a 24-hour time string "HH:MM".
	If iso_str is None or empty, return the current local time.
	"""
	fmt = "%H:%M"

	if not isinstance(iso_str, str):
		raise ValueError("iso_str must be a string or None")

	try:
		dt = datetime.fromisoformat(iso_str)
	except ValueError:
		dt = datetime.fromisoformat(iso_str.replace(" ", "T"))

	# Normalize to local timezone before formatting
	local_tz = datetime.now().astimezone().tzinfo
	if dt.tzinfo is None:
		dt = dt.replace(tzinfo=local_tz)
	dt = dt.astimezone(local_tz)

	return dt.strftime(fmt)


def generate_uuid() -> str:
	return str(uuid4()).split("-")[0]
