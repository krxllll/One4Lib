from pydantic import BaseModel, EmailStr, constr


class TokenUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    expires_in: int

class UserOut(BaseModel):
    id: str  # ObjectId as str
    username: str
    email: EmailStr
    role: str
    points: int
    is_banned: bool

    class Config:
        from_attributes = True


class RegisterPassword(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8)


class LoginPassword(BaseModel):
    email: EmailStr
    password: str


class OAuthToken(BaseModel):
    oauth_token: str  # id_token від Google або access_token GitHub