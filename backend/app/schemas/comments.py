from pydantic import BaseModel
from datetime import datetime

class CreateCommentRequest(BaseModel):
    file_id: str
    text: str

class CommentResponse(BaseModel):
    id: str
    user_id: str
    file_id: str
    text: str
    created_at: datetime
