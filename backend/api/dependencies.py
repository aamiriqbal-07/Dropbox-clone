from fastapi import Request, Depends
from repositories.file_repository import FileRepository
from services.storage.minio_storage import MinioStorage
from services.file_service import FileService
from core.database import get_db_connection

async def get_db_conn(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        yield conn

async def get_file_service(conn = Depends(get_db_conn)) -> FileService:
    repo = FileRepository(conn)
    storage = MinioStorage()
    return FileService(storage, repo)