from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.account.models import User
from app.core.security import decode_token
from app.core.exceptions import CredentialsException, PermissionDenied

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token)
        user_id = payload["sub"]
        oid = ObjectId(user_id)
    except Exception:
        raise CredentialsException()

    user = await User.get(oid)

    if not user or user.is_banned:
        raise CredentialsException()
    return user

# Optional authentication (returns None if no or invalid token)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_current_user_optional(token: str = Depends(oauth2_scheme_optional)) -> User | None:
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        oid = ObjectId(user_id)
        user = await User.get(oid)
        if not user or user.is_banned:
            return None
        return user
    except Exception:
        return None

async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise PermissionDenied()
    return user
