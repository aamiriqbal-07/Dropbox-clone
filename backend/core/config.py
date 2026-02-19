from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_use_ssl: bool = False
    
    log_file: str = "app.log"
    max_file_size: int = 10 * 1024 * 1024  # 10 MB

    class Config:
        env_file = ".env"

settings = Settings()