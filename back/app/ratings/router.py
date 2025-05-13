# app/ratings/router.py
from fastapi import APIRouter, Depends, status
from app.core.deps import get_current_user
from .schemas import RateRequest, AverageRatingResponse, UserRatingResponse
from .service import RatingService
from app.account.models import User

router = APIRouter(tags=["ratings"])

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def rate_file(
    req: RateRequest,
    current_user: User = Depends(get_current_user),
):
    await RatingService.rate_file(
        user_id=str(current_user.id),
        file_id=req.file_id,
        value=req.value,
    )

@router.get("/{file_id}/average", response_model=AverageRatingResponse)
async def average_rating(file_id: str):
    avg = await RatingService.get_average_rating(file_id)
    return AverageRatingResponse(average=avg)

@router.get("/{file_id}/user", response_model=UserRatingResponse)
async def user_rating(
    file_id: str,
    current_user: User = Depends(get_current_user),
):
    val = await RatingService.get_user_rating_for_file(
        user_id=str(current_user.id),
        file_id=file_id,
    )
    return UserRatingResponse(value=val)