from __future__ import annotations
from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field


class PointPurchaseTransaction(Document):
    """User buys site‑points via payment provider (Stripe / LiqPay)."""
    user_id: PydanticObjectId = Field(..., alias="userId")
    amount: int
    payment_method: str  # "card", "google_pay", etc.
    payment_meta: str | None = None  # last4 digits / txn id
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "point_purchase_tx"
        indexes = ["user_id"]

    class Config:
        allow_population_by_field_name = True


class PointRewardTransaction(Document):
    """System rewards points (e.g., +1 on upload)."""
    user_id: PydanticObjectId = Field(..., alias="userId")
    file_id: PydanticObjectId | None = Field(default=None, alias="fileId")
    amount: int
    reason: str  # "upload_reward", "promo_code" …
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "point_reward_tx"
        indexes = ["user_id"]

    class Config:
        allow_population_by_field_name = True
