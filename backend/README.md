# Dropbox-like Backend

A self‑hosted file storage backend with REST APIs. Built with FastAPI, MySQL (metadata), and MinIO (file storage). Designed to run in Docker containers.

## Features

- Upload, download, list, and delete files
- Metadata stored in MySQL
- Files stored in MinIO (S3‑compatible)
- Request ID tracing in logs
- CORS enabled for frontend access
- Containerized with Docker Compose

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository and navigate into the project folder:
   ```bash
   git clone <repo-url>
   cd dropbox-clone/backend
   ```

2. Create a `.env` file (or use the provided example):
   ```
   DB_HOST=mysql
   DB_PORT=3306
   DB_USER=admin
   DB_PASSWORD=12345
   DB_NAME=file_metadata

   MINIO_ENDPOINT=minio:9000
   MINIO_ACCESS_KEY=admin
   MINIO_SECRET_KEY=password123
   MINIO_BUCKET=myfiles
   MINIO_USE_SSL=false

   LOG_FILE=/app/logs/app.log
   MAX_FILE_SIZE=10485760
   ```

3. Run the entire stack with Docker Compose:
   ```bash
   docker-compose up -d
   ```

   This starts MySQL, MinIO, and the backend API. The backend will be available at `http://localhost:8000`.

4. Access the interactive API docs:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

All endpoints are prefixed with `/api/v1/files`.

### Upload a File
```
curl --location 'http://localhost:8000/api/v1/files/upload' \
--form 'file=@"/path/to/file"'
```

### List Files
```
curl --location 'http://localhost:8000/api/v1/files/?limit=10&offset=0'
```

### Download a File
```
curl --location 'http://localhost:8000/api/v1/files/9717b9a6-28bd-41cb-badf-fbe77994675a'
```

## Development Without Docker

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Make sure MySQL and MinIO are running (e.g., via Docker) and update `.env` with `localhost` as host.

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

```
.
├── api/                 # API routes (controllers)
├── core/                # Configuration, database, logging, middleware
├── models/              # Pydantic schemas
├── repositories/        # Data access layer
├── services/            # Business logic and storage abstraction
├── .env                 # Environment variables
├── main.py              # FastAPI application entry point
├── requirements.txt
└── Dockerfile

```
## License

[MIT](LICENSE)