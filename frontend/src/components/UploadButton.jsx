// src/components/UploadButton.jsx
import { useState } from 'react';
import { uploadFile } from '../services/api';
import { ACCEPT_STRING } from '../config';

export default function UploadButton({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const uploaded = await uploadFile(file);
      onUploadSuccess?.(uploaded);
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  return (
    <div>
      <input
        type="file"
        accept={ACCEPT_STRING}
        onChange={handleFileChange}
        disabled={uploading}
        id="file-upload"
        style={{ display: 'none' }}
      />
      <label htmlFor="file-upload" className="upload-button">
        {uploading ? 'Uploading...' : 'Upload File'}
      </label>
    </div>
  );
}