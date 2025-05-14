# app/files/schemas.py (updated)
from pydantic import BaseModel, constr
from typing import List
import datetime as _dt


class FileUploadRequest(BaseModel):
    title: str
    description: str | None = None
    file_type: str
    price: int = 0
    tags: List[constr(strip_whitespace=True, min_length=1)] = []


class FileResponse(BaseModel):
    id: str
    author_id: str
    title: str
    description: str | None
    file_type: str
    price: int
    tags: list[str]
    download_count: int
    purchase_count: int
    upload_date: _dt.datetime
    preview_url: str  # URL for preview image or placeholder


class SignedUrlResponse(BaseModel):
    url: str