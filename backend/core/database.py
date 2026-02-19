import aiomysql
import pymysql
from core.config import settings

async def ensure_database_exists():
    """Create the database if it doesn't exist."""
    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        charset='utf8mb4'
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.db_name}")
        connection.commit()
    finally:
        connection.close()

async def create_table_if_not_exists():
    """Create the files table if it doesn't exist."""
    # Use aiomysql with the target database
    pool = await aiomysql.create_pool(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
        autocommit=True
    )
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id CHAR(36) PRIMARY KEY,
                    original_name VARCHAR(255) NOT NULL,
                    stored_name VARCHAR(255) NOT NULL UNIQUE,
                    size BIGINT NOT NULL,
                    mime_type VARCHAR(127),
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX (upload_time)
                )
            """)
    pool.close()
    await pool.wait_closed()

async def get_db_pool():
    # First ensure database exists
    await ensure_database_exists()
    # Then create the table
    await create_table_if_not_exists()
    # Finally create and return the pool for normal operations
    pool = await aiomysql.create_pool(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
        autocommit=True,
        minsize=1,
        maxsize=10
    )
    return pool

async def get_db_connection():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        yield conn