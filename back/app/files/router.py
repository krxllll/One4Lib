from fastapi import APIRouter, Depends, UploadFile, File as FUpload
from bson import ObjectId

from app.core.deps import get_current_user
from .schemas import FileUploadRequest, FileResponse, SignedUrlResponse
from .service import FileService
from app.account.models import User

router = APIRouter(tags=["files"])

@router.post("/upload", response_model=str, status_code=201)
async def upload_file(
    meta: FileUploadRequest,
    raw_file: UploadFile = FUpload(...),
    current_user: User = Depends(get_current_user),
):
    user_id = str(current_user.id)
    file_id = await FileService.upload(user_id, meta, raw_file)
    return file_id

@router.get("/", response_model=list[FileResponse])
async def list_files(tags: list[str] | None = None):
    docs = await FileService.list_files(tags)
    return [FileResponse(**doc.dict(), id=str(doc.id)) for doc in docs]

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file_id: str):
    doc = await FileService.get_file(file_id)
    return FileResponse(**doc.dict(), id=str(doc.id))

@router.get("/{file_id}/download", response_model=SignedUrlResponse)
async def download_file(
    file_id: str,
    current_user = Depends(get_current_user),
):
    url = await FileService.generate_download_url(
        user_id=str(current_user.id),
        file_id=file_id
    )
    return SignedUrlResponse(url=url)
