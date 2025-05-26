from __future__ import annotations
from datetime import datetime, timezone
from typing import List
from beanie import Document
from pydantic import Field
from bson import ObjectId
from pydantic_mongo import ObjectIdField


class File(Document):
    """MongoDB document, зберігає лише метадані; сам файл у S3 (key)."""

    id: ObjectIdField = Field(default_factory=ObjectId, alias="_id")
    author_id: ObjectIdField
    file_key: str  # S3 object key
    file_type: str  # mime or enum
    title: str
    description: str | None = None
    tags: List[str] = Field(default_factory=list)
    price: int = 0  # points
    upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    purchase_count: int = 0

    class Settings:
        name = "files"
        indexes = ["author_id", "tags"]