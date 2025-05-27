from typing import List, Optional
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from io import BytesIO
from app.core.storage import create_signed_url, upload_fileobj
from app.models.file_purchase import FilePurchaseTransaction
from app.models.files import File
from app.services.points import PointsService
from app.services.preview import PreviewService
from app.schemas.files import FileUploadRequest, FileResponse
import asyncio

class FileService:

    @staticmethod
    async def upload(author_id: str, meta: FileUploadRequest, file) -> str:
        data = await file.read()
        thumb_bytes, prev_bytes = PreviewService.generate_variants(data, meta.file_type)

        async def _upl(data_bytes, content_type):
            return upload_fileobj(BytesIO(data_bytes), content_type)

        preview_content_type = file.content_type or meta.file_type

        original_key, thumbnail_key, preview_key = await asyncio.gather(
            _upl(data, file.content_type),
            _upl(thumb_bytes, "image/png") if thumb_bytes else None,
            _upl(prev_bytes, preview_content_type) if prev_bytes else None,
        )

        # 5) зберігаємо всі ключі
        doc = File(
            author_id=PydanticObjectId(author_id),
            file_key=original_key,
            thumbnail_key=thumbnail_key,
            preview_key=preview_key,
            file_type=meta.file_type,
            title=meta.title,
            description=meta.description or "",
            tags=meta.tags,
            price=meta.price,
        )
        await doc.insert()

        await PointsService.add_points_for_upload(author_id, str(doc.id))

        return str(doc.id)

    @staticmethod
    async def _is_purchased(uid: PydanticObjectId, fid: PydanticObjectId) -> bool:
        tx = await FilePurchaseTransaction.find_one({
            "user_id": uid,
            "file_id": fid
        })
        return tx is not None

    @staticmethod
    async def _build_response(
            doc: File,
            user_id: Optional[str],
            detail: bool = False
    ) -> FileResponse:
        # 1) визначаємо статус глядача
        if not user_id:
            viewer_status = "not_logged_in"
        else:
            uid = PydanticObjectId(user_id)
            if doc.author_id == uid:
                viewer_status = "author"
            elif await FileService._is_purchased(uid, doc.id):
                viewer_status = "owner"
            else:
                viewer_status = "logged_in"

        # 2) генеруємо URL-и
        # thumbnail завжди
        thumbnail_url = create_signed_url(doc.thumbnail_key) if doc.thumbnail_key else None

        # preview тільки у деталях
        preview_url = None
        file_url = None

        if detail:
            preview_url = create_signed_url(doc.preview_key) if doc.preview_key else None
            # оригінал — лише для автора або власника
            if viewer_status in ("author", "owner"):
                file_url = create_signed_url(doc.file_key)

        # 3) повертаємо FileResponse
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
            thumbnail_url=thumbnail_url,
            preview_url=preview_url,
            file_url=file_url,
            viewer_status=viewer_status,
        )

    @staticmethod
    async def list_files(
            user_id: Optional[str],
            filters: Optional[List[str]] = None,
            file_types: Optional[List[str]] = None,  # <- було file_type: Optional[str]
    ) -> List[FileResponse]:
        query: dict = {}
        if filters:
            query["tags"] = {"$all": filters}
        if file_types:
            query["file_type"] = {"$in": file_types}

        docs = await File.find(query).to_list()
        return [
            await FileService._build_response(doc, user_id, detail=False)
            for doc in docs
        ]

    @staticmethod
    async def get_file_detail(
            user_id: Optional[str],
            file_id: str
    ) -> FileResponse:
        # перетворюємо в PydanticObjectId для Beanie
        pid = PydanticObjectId(file_id)
        doc = await File.get(pid)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        # у деталях detail=True
        return await FileService._build_response(doc, user_id, detail=True)
