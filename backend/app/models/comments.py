from __future__ import annotations
from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field
from bson import ObjectId


class Comment(Document):
    """MongoDB документ для збереження коментарів."""
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: PydanticObjectId
    file_id: PydanticObjectId
    text: str = Field(..., alias="ftext")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "comments"
        indexes = ["user_id", "file_id"]