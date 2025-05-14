# app/files/router.py (updated)
from fastapi import APIRouter, Depends, UploadFile, File as FUpload, Form, HTTPException, status
from app.core.deps import get_current_user
from .schemas import FileUploadRequest, FileResponse, SignedUrlResponse
from .service import FileService
from app.account.models import User
from app.core.storage import create_signed_url
import json

router = APIRouter(tags=["files"])

@router.post("/upload", response_model=str, status_code=201)
async def upload_file(
    meta: str = Form(...),
    raw_file: UploadFile = FUpload(...),
    current_user: User = Depends(get_current_user),
):
    try:
        meta_obj = FileUploadRequest(**json.loads(meta))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid meta JSON: {e}"
        )
    file_id = await FileService.upload(str(current_user.id), meta_obj, raw_file)
    return file_id

@router.get("/", response_model=list[FileResponse])
async def list_files(tags: list[str] | None = None):
    docs = await FileService.list_files(tags)
    results: list[FileResponse] = []
    for doc in docs:
        # For now, preview is the signed URL of the original file
        preview = create_signed_url(doc.file_key)
        results.append(
            FileResponse(
                id=str(doc.id),
                author_id=str(doc.author_id),
                title=doc.title,
                description=doc.description,
                file_type=doc.file_type,
                price=doc.price,
                tags=doc.tags,
                download_count=doc.download_count,
                purchase_count=doc.purchase_count,
                upload_date=doc.upload_date,
                preview_url=preview,
            )
        )
    return results

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file_id: str):
    doc = await FileService.get_file(file_id)
    # For now, preview is the signed URL of the original file
    preview = create_signed_url(doc.file_key)
    return FileResponse(
        id=str(doc.id),
        author_id=str(doc.author_id),
        title=doc.title,
        description=doc.description,
        file_type=doc.file_type,
        price=doc.price,
        tags=doc.tags,
        download_count=doc.download_count,
        purchase_count=doc.purchase_count,
        upload_date=doc.upload_date,
        preview_url=preview,
    )

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