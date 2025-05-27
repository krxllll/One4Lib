from __future__ import annotations
from datetime import datetime, timezone
from beanie import Document, Indexed, PydanticObjectId
from pydantic import EmailStr, Field
from bson import ObjectId


class User(Document):
    """MongoDB user document (Beanie)."""

    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(max_length=30)
    email: Indexed(EmailStr, unique=True)
    password: str  # bcrypt‑hash
    role: str = "user"  # "user" | "admin"
    points: int = 0
    is_banned: bool = False
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"