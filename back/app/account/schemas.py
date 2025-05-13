# ============================================================
# schemas.py – Pydantic DTO
# ============================================================
from pydantic import BaseModel, EmailStr, constr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str  # ObjectId as str
    username: str
    email: EmailStr
    role: str
    points: int
    is_banned: bool

    class Config:
        orm_mode = True

class RegisterPassword(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8)

class LoginPassword(BaseModel):
    email: EmailStr
    password: str

class OAuthToken(BaseModel):
    oauth_token: str  # id_token від Google або access_token GitHub