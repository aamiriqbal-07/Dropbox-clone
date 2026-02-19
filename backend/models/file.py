from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileMetadataCreate(BaseModel):
    original_name: str
    size: int
    mime_type: Optional[str] = None

class FileMetadata(FileMetadataCreate):
    id: str
    stored_name: str
    upload_time: datetime

    class Config:
        from_attributes = True  # or orm_mode = True for Pydantic v1

class FileMetadataList(BaseModel):
    total: int
    files: list[FileMetadata]