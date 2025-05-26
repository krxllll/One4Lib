from fastapi import APIRouter, Depends, status, Response
from app.core.deps import get_current_user
from app.schemas.file_purchase import PurchaseFileRequest, TransactionResponse, BoughtFilesResponse
from app.services.file_purchase import FilePurchaseService
from app.models.account import User

router = APIRouter(tags=["purchase"])

@router.post("/file", status_code=status.HTTP_204_NO_CONTENT)
async def purchase_file(
    req: PurchaseFileRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Купівля файлу за поінти.
    Повертає 204, або 402 якщо недостатньо поінтів.
    """
    await FilePurchaseService.purchase_file(
        user_id=str(current_user.id),
        file_id=req.file_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/transactions/user", response_model=list[TransactionResponse])
async def user_transactions(
    current_user: User = Depends(get_current_user),
):
    txs = await FilePurchaseService.get_all_user_transactions(str(current_user.id))
    return [TransactionResponse(
        id=str(tx.id),
        date=tx.created_at,
        pointsSpent=tx.points_spent,
        userId=str(tx.user_id),
        fileId=str(tx.file_id),
    ) for tx in txs]

@router.get("/bought-files", response_model=BoughtFilesResponse)
async def bought_files(
    current_user: User = Depends(get_current_user),
):
    file_ids = await FilePurchaseService.get_bought_files(str(current_user.id))
    return BoughtFilesResponse(file_ids=file_ids)