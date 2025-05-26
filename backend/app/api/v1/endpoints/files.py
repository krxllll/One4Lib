import json
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File as FUpload, Form, HTTPException, status
from app.core.deps import get_current_user_optional
from app.schemas.files import FileUploadRequest, FileResponse
from app.services.files import FileService

router = APIRouter(tags=["files"])

@router.post("/upload", response_model=str, status_code=201)
async def upload_file(
    meta: str = Form(...),
    raw_file: UploadFile = FUpload(...),
    current_user=Depends(get_current_user_optional),
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        meta_obj = FileUploadRequest(**json.loads(meta))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid meta JSON: {e}"
        )
    return await FileService.upload(str(current_user.id), meta_obj, raw_file)

@router.get("/", response_model=list[FileResponse])
async def list_files(
    tags: Optional[List[str]] = Query(None),
    file_type: Optional[str] = Query(None),
    current_user=Depends(get_current_user_optional)
):
    user_id = str(current_user.id) if current_user else None
    return await FileService.list_files(user_id=user_id, filters=tags, file_type=file_type)

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    current_user=Depends(get_current_user_optional)
):
    user_id = str(current_user.id) if current_user else None
    return await FileService.get_file_detail(user_id=user_id, file_id=file_id)
