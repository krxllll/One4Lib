from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.account.models import User
from app.points.models import PointRewardTransaction

class CommissionService:
    """
    Нараховує автору комісію після покупки файлу.
    Використовує модель PointRewardTransaction з reason="author_commission".
    """
    BASE_COMMISSION_RATE = 10  # відсотків

    @classmethod
    async def distribute_commission(
        cls,
        author_id: str,
        file_id: str,
        total_price: int,
    ) -> None:
        aid = ObjectId(author_id)
        fid = ObjectId(file_id)

        # 1) Перевіряємо, що автор існує
        author = await User.get(aid)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

        # 2) Розраховуємо суму комісії
        commission_amount = (total_price * cls.BASE_COMMISSION_RATE) // 100
        if commission_amount <= 0:
            return

        # 3) Нараховуємо поінти автору
        await author.update({'$inc': {'points': commission_amount}})

        # 4) Логування транзакції комісії
        tx = PointRewardTransaction(
            user_id=aid,
            file_id=fid,
            amount=commission_amount,
            reason="author_commission",
            created_at=datetime.utcnow(),
        )
        await tx.insert()
