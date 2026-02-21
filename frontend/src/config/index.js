// Backend API base URL – change this to your backend address
export const API_BASE_URL = 'http://localhost:8000/api/v1';

// Allowed file types for upload – modify this array to restrict/allow types
// Each entry should be a valid MIME type
export const ALLOWED_FILE_TYPES = [
  'text/plain',
  'image/png',
  'image/jpeg',
  'application/json',
  'application/zip',
  'application/pdf'
];

// For the file input accept attribute, we can use extensions or MIME types
// We'll build a string from the above list
export const ACCEPT_STRING = ALLOWED_FILE_TYPES.join(',');