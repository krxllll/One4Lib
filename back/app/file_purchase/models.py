# app/file_purchase/models.py
from __future__ import annotations
import datetime as _dt
from beanie import Document
from pydantic import Field
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class FilePurchaseTransaction(Document):
    """Документ для збереження транзакцій покупки файлів за поінти."""
    id: ObjectIdField   = Field(default_factory=ObjectId, alias="_id")
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    points_spent: int
    user_id: ObjectIdField
    file_id: ObjectIdField

    class Settings:
        name = "file_purchase_transactions"
        indexes = ["user_id", "file_id"]