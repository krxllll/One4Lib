from fastapi import APIRouter, HTTPException, status
from app.schemas.account import RegisterPassword, LoginPassword, TokenUserResponse, OAuthToken
from app.services.account import AccountService
from app.models.account import User


router = APIRouter(tags=["auth"])

@router.post("/register", response_model=TokenUserResponse)
async def register_pw(data: RegisterPassword):
    token = await AccountService.register_password(data)
    # username у нас вже в data
    return TokenUserResponse(access_token=token, username=data.username)

@router.post("/login", response_model=TokenUserResponse)
async def login_pw(data: LoginPassword):
    token = await AccountService.login_password(data)
    # після успішного логіну знаходимо користувача, щоби взяти username
    user = await User.find_one(User.email == data.email)
    if not user:
        # таке навряд чи станеться, але на всяк випадок
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="User just logged-in but not found")
    return TokenUserResponse(access_token=token, username=user.username)

@router.post("/login/google", response_model=TokenUserResponse)
async def login_google(data: OAuthToken):
    token = await AccountService.auth_google(data)
    # отримуємо email з токена, далі username у базі
    email = await AccountService._verify_google(data.oauth_token)
    user = await User.find_one(User.email == email)
    return TokenUserResponse(access_token=token, username=user.username)

@router.post("/login/github", response_model=TokenUserResponse)
async def login_github(data: OAuthToken):
    token = await AccountService.auth_github(data)
    email = await AccountService._verify_github(data.oauth_token)
    user = await User.find_one(User.email == email)
    return TokenUserResponse(access_token=token, username=user.username)