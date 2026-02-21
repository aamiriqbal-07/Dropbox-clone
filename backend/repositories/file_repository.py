from uuid import uuid4
from datetime import datetime
from models.file import FileMetadata, FileMetadataCreate

class FileRepository:
    def __init__(self, db_conn):
        self.conn = db_conn

    async def create(self, file: FileMetadataCreate, stored_name: str) -> FileMetadata:
        file_id = str(uuid4())
        query = """
            INSERT INTO files (id, original_name, stored_name, size, mime_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, (
                file_id,
                file.original_name,
                stored_name,
                file.size,
                file.mime_type
            ))
        # Return the full metadata
        return FileMetadata(
            id=file_id,
            original_name=file.original_name,
            stored_name=stored_name,
            size=file.size,
            mime_type=file.mime_type,
            upload_time=datetime.utcnow()
        )

    async def get_by_id(self, file_id: str) -> FileMetadata | None:
        query = "SELECT id, original_name, stored_name, size, mime_type, upload_time FROM files WHERE id = %s"
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, (file_id,))
            row = await cursor.fetchone()
        if not row:
            return None
        return FileMetadata(
            id=row[0],
            original_name=row[1],
            stored_name=row[2],
            size=row[3],
            mime_type=row[4],
            upload_time=row[5]
        )

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[FileMetadata]:
        query = """
            SELECT id, original_name, stored_name, size, mime_type, upload_time
            FROM files
            ORDER BY upload_time DESC
            LIMIT %s OFFSET %s
        """
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, (limit, offset))
            rows = await cursor.fetchall()
        return [
            FileMetadata(
                id=r[0],
                original_name=r[1],
                stored_name=r[2],
                size=r[3],
                mime_type=r[4],
                upload_time=r[5]
            )
            for r in rows
        ]

    async def delete(self, file_id: str) -> bool:
        query = "DELETE FROM files WHERE id = %s"
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, (file_id,))
            return cursor.rowcount > 0