from pydantic import BaseModel, constr, Field, conint
from typing import List, Optional
import datetime as _dt


class FileUploadRequest(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str
    price: conint(ge=4) = 4
    tags: List[constr(strip_whitespace=True, min_length=1)] = []


class FileResponse(BaseModel):
    id: str
    author_id: str
    title: str
    description: Optional[str]
    file_type: str
    price: int
    tags: List[str]
    purchase_count: int
    upload_date: _dt.datetime

    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    file_url: Optional[str] = None

    viewer_status: str  # статус глядача: not_logged_in, logged_in, author, owner


class SignedUrlResponse(BaseModel):
    url: str