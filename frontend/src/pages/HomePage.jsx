// src/pages/HomePage.jsx
import { useState, useEffect, useCallback } from 'react';
import { fetchFiles } from '../services/api';
import FileList from '../components/FileList';
import Pagination from '../components/Pagination';
import UploadButton from '../components/UploadButton';
import './HomePage.css';

export default function HomePage() {
  const [files, setFiles] = useState([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(10);
  const [offset, setOffset] = useState(0);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadFiles = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchFiles(limit, offset);
      setFiles(data.files);
      setTotal(data.total);
      setSelectedFiles([]);
    } catch (err) {
      setError('Failed to load files: ' + err.message);
    } finally {
      setLoading(false);
    }
  }, [limit, offset]);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const handleFileSelect = (fileId, checked) => {
    setSelectedFiles(prev =>
      checked
        ? [...prev, fileId]
        : prev.filter(id => id !== fileId)
    );
  };

  const handleUploadSuccess = () => {
    loadFiles();
  };

  return (
    <div className="home-page">
      <h1>File Manager</h1>
      <UploadButton onUploadSuccess={handleUploadSuccess} />

      {loading && <p className="loading-message">Loading files...</p>}
      {error && <p className="error-message">{error}</p>}

      {!loading && !error && files.length === 0 ? (
        <div className="empty-state">
          <p>No files uploaded yet.</p>
          <p>Click the upload button above to add files (text, PNG, JPEG, JSON, ZIP).</p>
        </div>
      ) : (
        !loading && !error && (
          <>
            <FileList
              files={files}
              selectedFiles={selectedFiles}
              onFileSelect={handleFileSelect}
            />
            <Pagination
              total={total}
              limit={limit}
              offset={offset}
              onPageChange={setOffset}
            />
          </>
        )
      )}
    </div>
  );
}