
from datetime import datetime
from beanie import PydanticObjectId
from app.models.files import File
from app.models.file_purchase import FilePurchaseTransaction
from app.models.account import User
from fastapi import HTTPException, status
from app.services.points import PointsService


class FilePurchaseService:
    """Бізнес-логіка для покупки файлів за поінти"""

    @staticmethod
    async def purchase_file(user_id: str, file_id: str) -> None:
        uid = PydanticObjectId(user_id)
        fid = PydanticObjectId(file_id)

        # 1) Перевірка існування файлу
        f = await File.get(fid)
        if not f:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        # 2) Перевірка існування юзера
        u = await User.get(uid)
        if not u:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 3) Перевірка балансу
        if f.price > u.points:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Insufficient points. Please top up your balance."
            )

        # 4) Списання поінтів
        await u.update({'$inc': {'points': -f.price}})

        # 5) Інкремент лічильника покупок
        await f.update({'$inc': {'purchase_count': 1}})

        # 6) Запис транзакції
        tx = FilePurchaseTransaction(
            created_at=datetime.utcnow(),
            points_spent=f.price,
            user_id=uid,
            file_id=fid,
        )
        await tx.insert()

        # 7) Нарахування авторської комісії
        await PointsService.distribute_commission(
            author_id=str(f.author_id),
            file_id=file_id,
            total_price=f.price
        )

    @staticmethod
    async def get_all_user_transactions(user_id: str) -> list[FilePurchaseTransaction]:
        uid = PydanticObjectId(user_id)
        return await FilePurchaseTransaction.find(
            FilePurchaseTransaction.user_id == uid
        ).to_list()

    @staticmethod
    async def get_bought_files(user_id: str) -> list[str]:
        txs = await FilePurchaseService.get_all_user_transactions(user_id)
        return [str(tx.file_id) for tx in txs]
