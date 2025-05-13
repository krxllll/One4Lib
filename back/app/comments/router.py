# app/comments/router.py
from fastapi import APIRouter, Depends, status
from app.core.deps import get_current_user
from .schemas import CreateCommentRequest, CommentResponse
from .service import CommentService
from app.account.models import User

router = APIRouter(tags=["comments"])

@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def add_comment(
    req: CreateCommentRequest,
    current_user: User = Depends(get_current_user),
):
    return await CommentService.add_comment(
        user_id=str(current_user.id),
        file_id=req.file_id,
        text=req.text,
    )

@router.get("/user/{file_id}", response_model=list[str])
async def user_comments_for_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
):
    return await CommentService.get_user_comments_for_file(
        user_id=str(current_user.id),
        file_id=file_id,
    )

@router.get("/file/{file_id}", response_model=list[CommentResponse])
async def comments_for_file(
    file_id: str,
):
    comments = await CommentService.get_comments_for_file(file_id)
    return [CommentResponse(
        id=str(c.id),
        user_id=str(c.user_id),
        file_id=str(c.file_id),
        text=c.text,
        created_at=c.created_at,
    ) for c in comments]