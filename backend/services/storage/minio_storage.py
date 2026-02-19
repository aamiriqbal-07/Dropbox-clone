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

    async def save(self, file_data, object_name: str, content_type: str) -> str:
        """Upload file to MinIO using a thread to avoid blocking."""
        def _upload():
            # file_data is a synchronous file-like object after seek(0)
            self.client.put_object(
                self.bucket,
                object_name,
                file_data,
                length=-1,                # read until EOF
                content_type=content_type
            )
        await asyncio.to_thread(_upload)
        return object_name

    async def get(self, object_name: str):
        """Return an async generator that yields file chunks."""
        def _get_stream():
            return self.client.get_object(self.bucket, object_name)

        # Get the synchronous stream in a thread
        response = await asyncio.to_thread(_get_stream)

        async def chunk_generator():
            try:
                while True:
                    chunk = await asyncio.to_thread(response.read, 64 * 1024)  # 64KB chunks
                    if not chunk:
                        break
                    yield chunk
            finally:
                await asyncio.to_thread(response.close)
                await asyncio.to_thread(response.release_conn)

        return chunk_generator()

    async def delete(self, object_name: str):
        """Delete object from MinIO."""
        def _delete():
            self.client.remove_object(self.bucket, object_name)
        await asyncio.to_thread(_delete)