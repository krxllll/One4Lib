from __future__ import annotations
from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field
from bson import ObjectId


class Rating(Document):
    """MongoDB документ для збереження оцінок файлів."""
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: PydanticObjectId
    file_id: PydanticObjectId
    value: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "ratings"
        indexes = ["user_id", "file_id"]