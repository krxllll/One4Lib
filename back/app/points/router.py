from fastapi import APIRouter, Depends, status
from app.core.deps import get_current_user
from .schemas import PurchaseRequest, BalanceResponse, TransactionPublic
from .service import PointsService
from app.account.models import User

router = APIRouter(tags=["points"])

@router.post("/purchase", status_code=status.HTTP_201_CREATED)
async def buy_points(
    req: PurchaseRequest,
    current_user: User = Depends(get_current_user),
):
    user_id = str(current_user.id)
    await PointsService.purchase_points(user_id, req)
    return {"detail": "OK"}

@router.get("/balance", response_model=BalanceResponse)
async def balance(
    current_user: User = Depends(get_current_user),
):
    user_id = str(current_user.id)
    bal = await PointsService.get_balance(user_id)
    return {"balance": bal}

@router.get("/transactions", response_model=list[TransactionPublic])
async def transactions(
    current_user: User = Depends(get_current_user),
):
    user_id = str(current_user.id)
    return await PointsService.list_transactions(user_id)
