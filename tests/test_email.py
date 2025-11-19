import pytest

from src.auth.service_email import EmailService


@pytest.fixture()
def email_service():
	email_service = EmailService()
	return email_service


def test_send_email(email_service):
	otp = "12345"
	email = "lemanh1412@gmail.com"
	result = email_service.send_otp_email(email=email,otp=otp)
