# File Manager Frontend

A React-based frontend for a file management backend. Built with Vite.

## Features

- List files with pagination
- Upload files (restricted to configurable types: text, PNG, JPEG, JSON, ZIP)
- Download individual or multiple selected files
- View file content (if browser supports preview: images, text, JSON)
- Responsive design with modular components

## Configuration

All configuration is in `src/config/index.js`:

- `API_BASE_URL`: Backend API endpoint (default: `/api/v1` with Vite proxy for development)
- `ALLOWED_FILE_TYPES`: Array of MIME types for upload restrictions
- `ACCEPT_STRING`: Automatically generated input accept attribute

## Development

```bash
npm install
npm run dev
```

The dev server runs on `http://localhost:5173` and proxies API requests to `http://localhost:8000` (configured in `vite.config.js`).

## Production Build

```bash
npm run build
```

The output will be in the `dist` folder.

## Docker

Build the image:

```bash
docker build -t file-manager-frontend .
```

Run with:

```bash
docker run -p 8080:80 file-manager-frontend
```

The app will be available at `http://localhost:8080`.

## Environment Variables (for Docker)

- `VITE_API_BASE_URL`: Backend URL (e.g., `http://backend:8000/api/v1`). Pass at build time.

Example build:

```bash
docker build --build-arg VITE_API_BASE_URL=http://backend:8000/api/v1 -t file-manager-frontend .
```

## Project Structure

```
src/
├── config/          # Configuration (API URL, allowed types)
├── services/        # API calls
├── components/      # Reusable UI components
├── pages/           # HomePage and FileDetailPage
├── App.jsx          # Routing
└── main.jsx         # Entry point
```
