import jwt
import httpx
from pydantic import EmailStr
from app.core.security import hash_password, verify_password, create_token
from app.core.exceptions import CredentialsException
from app.schemas.account import RegisterPassword, LoginPassword, OAuthToken
from app.models.account import User


class AccountService:
    """Логіка реєстрації / логіну через Beanie ODM"""

    @staticmethod
    async def _email_exists(email: str) -> bool:
        return await User.find_one(User.email == email) is not None

    @staticmethod
    async def register_password(data: RegisterPassword) -> str:
        if await AccountService._email_exists(data.email):
            raise CredentialsException("Email already registered")
        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
        )
        await user.insert()
        return create_token(str(user.id), user.role)

    @staticmethod
    async def login_password(data: LoginPassword) -> str:
        user = await User.find_one(User.email == data.email)
        if not user or not verify_password(data.password, user.password):
            raise CredentialsException("Invalid credentials")
        return create_token(str(user.id), user.role)

    @staticmethod
    async def _verify_google(id_token: str) -> EmailStr:
        try:
            header = jwt.get_unverified_header(id_token)
            if header.get("alg") != "RS256":
                raise ValueError()
            payload = jwt.decode(id_token, options={"verify_signature": False})
            return payload["email"]
        except Exception:
            raise CredentialsException("Google token verification failed")

    @staticmethod
    async def auth_google(token: OAuthToken) -> str:
        email = await AccountService._verify_google(token.oauth_token)
        user = await User.find_one(User.email == email)
        if not user:
            user = User(
                username=email.split("@")[0],
                email=email,
                password="",  # no password for OAuth
            )
            await user.insert()
        return create_token(str(user.id), user.role)

    @staticmethod
    async def _verify_github(access_token: str) -> EmailStr:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"token {access_token}"},
                timeout=10,
            )
        if response.status_code != 200:
            raise CredentialsException("GitHub token verification failed")
        emails = response.json()
        primary = next((e for e in emails if e.get("primary")), None)
        if not primary or not primary.get("email"):
            raise CredentialsException("No primary email found for GitHub user")
        return primary["email"]

    @staticmethod
    async def auth_github(token: OAuthToken) -> str:
        email = await AccountService._verify_github(token.oauth_token)
        user = await User.find_one(User.email == email)
        if not user:
            user = User(
                username=email.split("@")[0],
                email=email,
                password="",
            )
            await user.insert()
        return create_token(str(user.id), user.role)
