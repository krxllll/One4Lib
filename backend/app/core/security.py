from datetime import datetime, timedelta
from typing import Any, Dict
import jwt
from passlib.context import CryptContext
from .config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return _pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return _pwd_context.verify(password, hashed)

def create_token(sub: str, role: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_exp_minutes))
    payload: Dict[str, Any] = {"sub": sub, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
