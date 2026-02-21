# Dropbox-like File Storage with FastAPI, MySQL, MinIO, and React Frontend

A complete self‑hosted file storage solution.  
- **Backend**: FastAPI (Python) – provides REST APIs for file upload/download/listing/deletion.  
- **Frontend**: React (Vite) – a simple UI to interact with the backend.  
- **Database**: MySQL – stores file metadata.  
- **Object Storage**: MinIO – stores the actual files.

All services are containerized with Docker Compose for easy setup.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

---

## Quick Start

1. **Clone the repository**  
   ```bash
   git@github.com:aamiriqbal-07/Dropbox-clone.git
   cd Dropbix-clone
   ```

2. **Start all services**  
   ```bash
   docker-compose up -d
   ```
   This builds and starts:
   - MySQL (port 3307)
   - MinIO (ports 9000 API, 9001 console)
   - Backend (port 8000)
   - Frontend (port 8080)

3. **Check that everything is running**  
   ```bash
   docker-compose ps
   ```
   All services should show `Up`.

4. **Access the applications**  
   - **Backend API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - **Frontend UI**: [http://localhost:8080](http://localhost:8080)  
   - **MinIO Console**: [http://localhost:9001](http://localhost:9001) (login: `admin` / `password123`)  
   - **MySQL**: connect on `localhost:3307` with user `admin`, password `12345`, database `file_metadata`.

---

## Environment Configuration

All required environment variables are set directly in the `docker-compose.yml` file.  
The backend `.env` file is **ignored** inside the container (thanks to a `.dockerignore` file).  
If you need to change any setting (e.g., file size limit), edit the `environment` section under the `backend` service in `docker-compose.yml`.

---

## Stopping and Cleaning Up

- Stop all containers:
  ```bash
  docker-compose down
  ```
- Remove volumes (deletes all stored files and database data):
  ```bash
  docker-compose down -v
  ```

## NOTE: Readme for backend and frontend have been provided here:

- Backend Readme file:
  [Link here](https://github.com/aamiriqbal-07/Dropbox-clone/blob/main/backend/README.md)

- Frontnd Readme file:
  [Link here](https://github.com/aamiriqbal-07/Dropbox-clone/blob/main/frontend/README.md)

## License

MIT