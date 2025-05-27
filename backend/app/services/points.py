from fastapi import HTTPException, status
from app.models.account import User
from app.models.points import PointRewardTransaction, PointPurchaseTransaction
from app.schemas.points import PurchaseRequest, TransactionPublic
from datetime import datetime
from beanie import PydanticObjectId


class PointsService:
    REWARD_ON_UPLOAD = 1
    BASE_COMMISSION_RATE = 10  # відсотків

    @staticmethod
    async def add_points_for_upload(user_id: str, file_id: str) -> None:
        # 1) знайти користувача
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        # 2) додати бали
        await user.update({'$inc': {'points': PointsService.REWARD_ON_UPLOAD}})
        # 3) записати транзакцію винагороди
        tx = PointRewardTransaction(
            userId=PydanticObjectId(user_id),
            fileId=PydanticObjectId(file_id),
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
        aid = PydanticObjectId(author_id)
        fid = PydanticObjectId(file_id)

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
            userId=aid,
            fileId=fid,
            amount=commission_amount,
            reason="author_commission",
            created_at=datetime.utcnow(),
        )
        await tx.insert()

    @staticmethod
    async def purchase_points(user_id: str, req: PurchaseRequest) -> None:
        # TODO: verify payment via external provider
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        await user.update({'$inc': {'points': req.amount}})
        tx = PointPurchaseTransaction(
            userId=PydanticObjectId(user_id),
            amount=req.amount,
            payment_method=req.payment_method,
            payment_meta=req.payment_token[-4:],
        )
        await tx.insert()

    @staticmethod
    async def get_balance(user_id: str) -> int:
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.points

    @staticmethod
    async def list_transactions(user_id: str) -> list[TransactionPublic]:
        uid = PydanticObjectId(user_id)
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
