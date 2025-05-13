# app/ratings/models.py
from __future__ import annotations
import datetime as _dt
from beanie import Document
from pydantic import Field
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class Rating(Document):
    """MongoDB документ для збереження оцінок файлів."""
    id:      ObjectIdField      = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectIdField
    file_id: ObjectIdField
    value:   int
    created_at: _dt.datetime    = Field(default_factory=_dt.datetime.utcnow)

    class Settings:
        name = "ratings"
        indexes = ["user_id", "file_id"]
