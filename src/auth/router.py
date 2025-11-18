
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_auth_service
from src.auth.model import Token
from src.auth.service import AuthService

router = APIRouter()
@router.post("/login", response_model=Token)
async def login(
		form_data: OAuth2PasswordRequestForm = Depends(),
		auth_service: AuthService = Depends(get_auth_service),
):
	access_token = await auth_service.authenticate_user(form_data.username, form_data.password)
	return {"access_token": access_token, "token_type": "bearer"}