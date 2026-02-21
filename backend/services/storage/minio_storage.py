import asyncio
from minio import Minio
from core.config import settings
from services.storage.base import Storage

class MinioStorage(Storage):
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_use_ssl
        )
        self.bucket = settings.minio_bucket

    async def save(self, file_data, object_name: str, content_type: str, size: int = None) -> str:
        def _upload():
            if size is not None:
                # Known size
                self.client.put_object(
                    self.bucket,
                    object_name,
                    file_data,
                    length=size,
                    content_type=content_type
                )
            else:
                self.client.put_object(
                    self.bucket,
                    object_name,
                    file_data,
                    length=-1,
                    part_size=10 * 1024 * 1024,
                    content_type=content_type
                )
        await asyncio.to_thread(_upload)
        return object_name

    async def get(self, object_name: str):
        def _get_stream():
            return self.client.get_object(self.bucket, object_name)

        response = await asyncio.to_thread(_get_stream)

        async def chunk_generator():
            try:
                while True:
                    chunk = await asyncio.to_thread(response.read, 64 * 1024)
                    if not chunk:
                        break
                    yield chunk
            finally:
                await asyncio.to_thread(response.close)
                await asyncio.to_thread(response.release_conn)

        return chunk_generator()

    async def delete(self, object_name: str):
        def _delete():
            self.client.remove_object(self.bucket, object_name)
        await asyncio.to_thread(_delete)