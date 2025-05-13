from fastapi import UploadFile, HTTPException, status
from bson import ObjectId

from app.core.storage import upload_fileobj, create_signed_url
from .models import File
from .schemas import FileUploadRequest
from app.file_purchase.models import FilePurchaseTransaction


class FileService:
    @staticmethod
    async def upload(author_id: str, meta: FileUploadRequest, file: UploadFile) -> str:
        # TODO: hook AI-moderator -> validate file
        key = upload_fileobj(file.file, file.content_type or "application/octet-stream")
        doc = File(
            author_id=ObjectId(author_id),
            file_key=key,
            file_type=meta.file_type,
            title=meta.title,
            description=meta.description,
            tags=meta.tags,
            price=meta.price,
        )
        await doc.insert()
        return str(doc.id)

    @staticmethod
    async def get_file(file_id: str) -> File:
        obj_id = ObjectId(file_id)
        doc = await File.get(obj_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return doc

    @staticmethod
    async def list_files(filters: list[str] | None = None) -> list[File]:
        if filters:
            cursor = File.find({"tags": {"$all": filters}})
        else:
            cursor = File.find()
        return await cursor.to_list()

    @staticmethod
    async def generate_download_url(user_id: str, file_id: str) -> str:
        uid = ObjectId(user_id)
        fid = ObjectId(file_id)

        # 1) Load the File metadata
        f = await File.get(fid)
        if not f:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")

        # 2) If you’re the author, free pass
        if f.author_id == uid:
            # increment count
            await f.update({'$inc': {'download_count': 1}})
            return create_signed_url(f.file_key)

        # 3) Otherwise check purchase record
        bought = await FilePurchaseTransaction.find_one(
            (FilePurchaseTransaction.user_id == uid) &
            (FilePurchaseTransaction.file_id == fid)
        )
        if not bought:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                "You must purchase this file before downloading")

        # 4) Count & sign
        await f.update({'$inc': {'download_count': 1}})
        return create_signed_url(f.file_key)
