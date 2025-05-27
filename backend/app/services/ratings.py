from bson import ObjectId
import datetime as _dt
from app.models.ratings import Rating
from beanie import PydanticObjectId


class RatingService:
    """Бізнес-логіка для оцінювання файлів"""

    @staticmethod
    async def rate_file(user_id: str, file_id: str, value: int) -> None:
        uid = PydanticObjectId(user_id)
        fid = PydanticObjectId(file_id)
        now = _dt.datetime.utcnow()
        existing = await Rating.find_one({"user_id": uid, "file_id": fid})
        if existing:
            # оновлюємо значення та час
            await existing.update({'$set': {'value': value, 'created_at': now}})
        else:
            r = Rating(user_id=uid, file_id=fid, value=value, created_at=now)
            await r.insert()

    @staticmethod
    async def get_average_rating(file_id: str) -> float:
        fid = ObjectId(file_id)
        docs = await Rating.find(Rating.file_id == fid).to_list()
        if not docs:
            return 0.0
        total = sum(r.value for r in docs)
        return total / len(docs)

    @staticmethod
    async def get_user_rating_for_file(user_id: str, file_id: str) -> int:
        uid = ObjectId(user_id)
        fid = ObjectId(file_id)
        r = await Rating.find_one({"user_id": uid, "file_id": fid})
        return r.value if r else 0