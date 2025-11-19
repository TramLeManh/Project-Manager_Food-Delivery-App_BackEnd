from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_auth_service
from src.auth.model import Token, OTPResponse, OTPRequest, OTPVerify, PasswordReset
from src.auth.service_auth import AuthService
from src.core.models_response import success

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
		form_data: OAuth2PasswordRequestForm = Depends(),
		auth_service: AuthService = Depends(get_auth_service),
):
	access_token = await auth_service.authenticate_user(form_data.username, form_data.password)
	return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-otp", response_model=OTPResponse)
async def request_otp(
		request: OTPRequest,
		auth_service: AuthService = Depends(get_auth_service),
):
	data = await auth_service.request_otp(str(request.email))
	message = "OTP sent successfully to your email"
	return success(data=data, message=message)


@router.post("/verify-otp")
async def verify_otp(
		request: OTPVerify,
		auth_service: AuthService = Depends(get_auth_service),
):
	auth_service.verify_otp(session_id=request.session_id, otp=request.otp)
	message = "OTP verified successfully. You can now reset your password."
	return success(message=message)


@router.post("/reset-password")
async def verify_otp(
		request: PasswordReset,
		auth_service: AuthService = Depends(get_auth_service),
):
	data = await auth_service.reset_password(session_id=request.session_id, new_password=request.password)
	message = "Password reset successfully"
	return success(message=message)
