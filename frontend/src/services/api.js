import { API_BASE_URL } from '../config';

export async function fetchFiles(limit = 10, offset = 0) {
  const url = `${API_BASE_URL}/files/?limit=${limit}&offset=${offset}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to fetch files');
  return response.json();
}

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${API_BASE_URL}/files/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) throw new Error('Upload failed');
  return response.json();
}

export async function downloadFile(fileId, fileName) {
  const response = await fetch(`${API_BASE_URL}/files/${fileId}`);
  if (!response.ok) throw new Error('Download failed');
  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export async function fetchFileBlob(fileId) {
  const response = await fetch(`${API_BASE_URL}/files/${fileId}`);
  if (!response.ok) throw new Error('Failed to fetch file');
  return response.blob();
}