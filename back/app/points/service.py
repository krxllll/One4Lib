from fastapi import HTTPException, status
from bson import ObjectId

from app.account.models import User
from app.files.models import File
from app.points.models import PointPurchaseTransaction, PointRewardTransaction
from app.points.schemas import PurchaseRequest, TransactionPublic


class PointsService:
    REWARD_ON_UPLOAD = 4

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
