import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from repositories.file_repository import FileRepository
from services.storage.base import Storage
from models.file import FileMetadata, FileMetadataCreate

class FileService:
    def __init__(self, storage: Storage, repo: FileRepository):
        self.storage = storage
        self.repo = repo

    async def upload_file(self, file: UploadFile, max_size: int) -> FileMetadata:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        await file.seek(0)
        if size > max_size:
            raise HTTPException(status_code=413, detail="File too large")

        ext = os.path.splitext(file.filename)[1]
        stored_name = f"{uuid4().hex}{ext}"

        # Pass the size to storage.save()
        await self.storage.save(
            file.file,
            stored_name,
            file.content_type or "application/octet-stream",
            size=size
        )

        meta_create = FileMetadataCreate(
            original_name=file.filename,
            size=size,
            mime_type=file.content_type
        )
        metadata = await self.repo.create(meta_create, stored_name)
        return metadata

    async def download_file(self, file_id: str):
        meta = await self.repo.get_by_id(file_id)
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        stream = await self.storage.get(meta.stored_name)
        return stream, meta

    async def list_files(self, limit: int, offset: int) -> list[FileMetadata]:
        return await self.repo.list_all(limit, offset)

    async def delete_file(self, file_id: str):
        meta = await self.repo.get_by_id(file_id)
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        await self.storage.delete(meta.stored_name)
        await self.repo.delete(file_id)