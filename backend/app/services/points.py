from fastapi import HTTPException, status
from bson import ObjectId
from app.models.account import User
from app.models.points import PointRewardTransaction, PointPurchaseTransaction
from app.schemas.points import PurchaseRequest, TransactionPublic
from datetime import datetime


class PointsService:
    REWARD_ON_UPLOAD = 4
    BASE_COMMISSION_RATE = 10  # відсотків

    @staticmethod
    async def add_points_for_upload(user_id: str, file_id: str) -> None:
        # 1) знайти користувача
        user = await User.get(ObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        # 2) додати бали
        await user.update({'$inc': {'points': PointsService.REWARD_ON_UPLOAD}})
        # 3) записати транзакцію винагороди
        tx = PointRewardTransaction(
            user_id=ObjectId(user_id),
            file_id=ObjectId(file_id),
            amount=PointsService.REWARD_ON_UPLOAD,
            reason="upload_reward",
        )
        await tx.insert()

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

    @staticmethod
    async def purchase_points(user_id: str, req: PurchaseRequest) -> None:
        # TODO: verify payment via external provider
        user = await User.get(ObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        await user.update({'$inc': {'points': req.amount}})
        tx = PointPurchaseTransaction(
            user_id=ObjectId(user_id),
            amount=req.amount,
            payment_method=req.payment_method,
            payment_meta=req.payment_token[-4:],
        )
        await tx.insert()

    @staticmethod
    async def get_balance(user_id: str) -> int:
        user = await User.get(ObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.points

    @staticmethod
    async def list_transactions(user_id: str) -> list[TransactionPublic]:
        uid = ObjectId(user_id)
        purchases = await PointPurchaseTransaction.find(
            PointPurchaseTransaction.user_id == uid
        ).to_list()
        rewards = await PointRewardTransaction.find(
            PointRewardTransaction.user_id == uid
        ).to_list()
        # Об’єднати та відсортувати за датою створення
        combined = purchases + rewards
        combined.sort(key=lambda tx: tx.created_at, reverse=True)

        public_list: list[TransactionPublic] = []
        for tx in combined:
            public_list.append(
                TransactionPublic(
                    id=str(tx.id),
                    amount=tx.amount,
                    payment_method=getattr(tx, 'payment_method', None),
                    reason=getattr(tx, 'reason', None),
                    created_at=tx.created_at,
                )
            )
        return public_list
