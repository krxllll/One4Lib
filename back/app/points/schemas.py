# ============================================================
# schemas.py
# ============================================================
from pydantic import BaseModel, Field
import datetime as _dt

class PurchaseRequest(BaseModel):
    amount: int = Field(gt=0)
    payment_method: str
    payment_token: str  # token від платіжної системи

class BalanceResponse(BaseModel):
    balance: int

class TransactionPublic(BaseModel):
    id: str
    amount: int
    reason: str | None = None
    payment_method: str | None = None
    created_at: _dt.datetime