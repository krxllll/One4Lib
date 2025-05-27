from __future__ import annotations
from datetime import datetime, timezone
from typing import List
from beanie import Document, PydanticObjectId
from pydantic import Field, conint
from bson import ObjectId


class File(Document):
    """MongoDB document, зберігає лише метадані; сам файл у S3 (key)."""

    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    author_id: PydanticObjectId
    file_key: str  # S3 object key
    thumbnail_key: str # S3 object key
    preview_key: str # S3 object key
    file_type: str # "image" | "video" | "audio" | "document" | "archive"
    title: str
    description: str | None = None
    tags: List[str] = Field(default_factory=list) # ["tag1", "tag2"]
    price: conint(ge=4) = 4 # points
    upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    purchase_count: int = 0

    class Settings:
        name = "files"
        indexes = ["author_id", "tags"]