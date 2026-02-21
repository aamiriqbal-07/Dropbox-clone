from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from starlette.responses import StreamingResponse
from services.file_service import FileService
from api.dependencies import get_file_service
from models.file import FileMetadata, FileMetadataList
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/files", tags=["files"])

@router.post("/upload", response_model=FileMetadata, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service)
):
    logger.info(f"Uploading file: {file.filename}")
    try:
        result = await service.upload_file(file, max_size=10*1024*1024)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=FileMetadataList)
async def list_files(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: FileService = Depends(get_file_service)
):
    files = await service.list_files(limit, offset)
    return {"total": len(files), "files": files}

@router.get("/{file_id}")
async def download_file(
    file_id: str,
    service: FileService = Depends(get_file_service)
):
    stream, meta = await service.download_file(file_id)
    return StreamingResponse(
        stream,
        media_type=meta.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename=\"{meta.original_name}\"",
            "Content-Length": str(meta.size)
        }
    )

@router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: str,
    service: FileService = Depends(get_file_service)
):
    await service.delete_file(file_id)
    return