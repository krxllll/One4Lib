# app/files/service.py
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status

from app.core.storage import create_signed_url, upload_fileobj
from app.file_purchase.models import FilePurchaseTransaction
from .models import File
from .schemas import FileUploadRequest, FileResponse

class FileService:
    @staticmethod
    async def upload(author_id: str, meta: FileUploadRequest, file) -> str:
        key = upload_fileobj(file.file, file.content_type or "application/octet-stream")
        doc = File(
            author_id=ObjectId(author_id),
            file_key=key,
            file_type=meta.file_type,
            title=meta.title,
            description=meta.description or "",
            tags=meta.tags,
            price=meta.price,
        )
        await doc.insert()
        return str(doc.id)

    @staticmethod
    async def _is_purchased(uid: ObjectId, fid: ObjectId) -> bool:
        tx = await FilePurchaseTransaction.find_one({
            "user_id": uid,
            "file_id": fid
        })
        return tx is not None

    @staticmethod
    async def _build_response(doc: File, user_id: Optional[str]) -> FileResponse:
        # визначаємо статус глядача
        if not user_id:
            viewer_status = "not_logged_in"
        else:
            uid = ObjectId(user_id)
            if doc.author_id == uid:
                viewer_status = "author"
            elif await FileService._is_purchased(uid, doc.id):
                viewer_status = "owner"
            else:
                viewer_status = "logged_in"
        # TODO: якщо viewer_status in ("not_logged_in","logged_in") => генерувати preview_key
        url = create_signed_url(doc.file_key)

        return FileResponse(
            id=str(doc.id),
            author_id=str(doc.author_id),
            title=doc.title,
            description=doc.description,
            file_type=doc.file_type,
            price=doc.price,
            tags=doc.tags,
            purchase_count=doc.purchase_count,
            upload_date=doc.upload_date,
            file_url=url,
            viewer_status=viewer_status,
        )

    @staticmethod
    async def list_files(
        user_id: Optional[str],
        filters: Optional[List[str]] = None,
        file_type: Optional[str] = None
    ) -> List[FileResponse]:
        query: dict = {}
        if filters:
            query["tags"] = {"$all": filters}
        if file_type:
            query["file_type"] = file_type
        docs = await File.find(query).to_list()

        # будуємо відповіді без повторного запиту до БД
        return [await FileService._build_response(doc, user_id) for doc in docs]

    @staticmethod
    async def get_file_detail(
        user_id: Optional[str],
        file_id: str
    ) -> FileResponse:
        doc = await File.get(ObjectId(file_id))
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return await FileService._build_response(doc, user_id)
