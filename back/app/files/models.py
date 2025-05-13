# ============================================================
# models.py
# ============================================================
from __future__ import annotations
import datetime as _dt
from typing import List, Optional
from beanie import Document, Indexed
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
    description: str
    tags: List[str] = []
    price: int = 0  # points
    upload_date: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    download_count: int = 0
    purchase_count: int = 0

    class Settings:
        name = "files"
        indexes = ["author_id", "tags"]