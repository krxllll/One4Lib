from __future__ import annotations
import datetime as _dt
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class User(Document):
    """MongoDB user document (Beanie)."""

    id: ObjectIdField = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(max_length=30)
    email: Indexed(EmailStr, unique=True)
    password: str  # bcrypt‑hash
    role: str = "user"  # "user" | "admin"
    points: int = 0
    is_banned: bool = False
    registered_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    class Settings:
        name = "users"
