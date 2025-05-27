from pydantic import BaseModel, Field


class RateRequest(BaseModel):
    file_id: str
    value: int = Field(..., ge=1, le=10)


class AverageRatingResponse(BaseModel):
    average: float


class UserRatingResponse(BaseModel):
    value: int