from __future__ import annotations
import datetime as _dt
from beanie import Document
from pydantic import Field
from pydantic_mongo import ObjectIdField


class PointPurchaseTransaction(Document):
    """User buys site‑points via payment provider (Stripe / LiqPay)."""
    user_id: ObjectIdField = Field(..., alias="userId")
    amount: int
    payment_method: str  # "card", "google_pay", etc.
    payment_meta: str | None = None  # last4 digits / txn id
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    class Settings:
        name = "point_purchase_tx"
        indexes = ["user_id"]


class PointRewardTransaction(Document):
    """System rewards points (e.g., +4 on upload)."""
    user_id: ObjectIdField = Field(..., alias="userId")
    file_id: ObjectIdField | None = Field(default=None, alias="fileId")
    amount: int
    reason: str  # "upload_reward", "promo_code" …
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    class Settings:
        name = "point_reward_tx"
        indexes = ["user_id"]
