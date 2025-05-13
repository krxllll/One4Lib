# app/file_purchase/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime


class PurchaseFileRequest(BaseModel):
    file_id: str


class TransactionResponse(BaseModel):
    id: str
    date: datetime
    points_spent: int = Field(..., alias="pointsSpent")
    user_id: str     = Field(..., alias="userId")
    file_id: str     = Field(..., alias="fileId")


class BoughtFilesResponse(BaseModel):
    file_ids: list[str]