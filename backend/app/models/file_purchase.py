from __future__ import annotations
from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field
from bson import ObjectId


class FilePurchaseTransaction(Document):
    """Документ для збереження транзакцій покупки файлів за поінти."""
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    points_spent: int
    user_id: PydanticObjectId
    file_id: PydanticObjectId

    class Settings:
        name = "file_purchase_transactions"
        indexes = ["user_id", "file_id"]