# ============================================================
# router.py – API endpoints
# ============================================================
from fastapi import APIRouter, Depends
from app.account.schemas import (
    RegisterPassword,
    LoginPassword,
    OAuthToken,
    TokenResponse,
)
from app.account.service import AccountService

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register_pw(data: RegisterPassword):
    token = await AccountService.register_password(data)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login_pw(data: LoginPassword):
    token = await AccountService.login_password(data)
    return TokenResponse(access_token=token)

@router.post("/login/google", response_model=TokenResponse)
async def login_google(data: OAuthToken):
    token = await AccountService.auth_google(data)
    return TokenResponse(access_token=token)

@router.post("/login/github", response_model=TokenResponse)
async def login_github(data: OAuthToken):
    token = await AccountService.auth_github(data)
    return TokenResponse(access_token=token)