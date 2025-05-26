from bson import ObjectId
from app.models.comments import Comment


class CommentService:
    """Бізнес-логіка для коментарів"""

    @staticmethod
    async def add_comment(user_id: str, file_id: str, text: str) -> str:
        c = Comment(
            user_id=ObjectId(user_id),
            file_id=ObjectId(file_id),
            text=text,
        )
        await c.insert()
        return str(c.id)

    @staticmethod
    async def get_user_comments_for_file(user_id: str, file_id: str) -> list[str]:
        docs = await Comment.find(
            Comment.user_id == ObjectId(user_id),
            Comment.file_id == ObjectId(file_id)
        ).to_list()
        return [doc.text for doc in docs]

    @staticmethod
    async def get_comments_for_file(file_id: str) -> list[Comment]:
        return await Comment.find(
            Comment.file_id == ObjectId(file_id)
        ).to_list()