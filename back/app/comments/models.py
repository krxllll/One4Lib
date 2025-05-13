from __future__ import annotations
import datetime as _dt
from beanie import Document
from pydantic import Field
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class Comment(Document):
    """MongoDB документ для збереження коментарів."""
    id: ObjectIdField = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectIdField
    file_id: ObjectIdField
    text: str = Field(..., alias="ftext")
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    class Settings:
        name = "comments"
        indexes = ["user_id", "file_id"]


