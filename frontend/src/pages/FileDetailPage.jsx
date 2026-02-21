// src/pages/FileDetailPage.jsx
import { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { fetchFileBlob, downloadFile, fetchFiles } from '../services/api';

export default function FileDetailPage() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [file, setFile] = useState(location.state?.file || null);
  const [content, setContent] = useState(null);
  const [contentType, setContentType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadFileAndContent() {
      try {
        let fileMeta = file;
        if (!fileMeta) {
          const data = await fetchFiles(100, 0);
          const found = data.files.find(f => f.id === id);
          if (!found) throw new Error('File not found');
          fileMeta = found;
          setFile(fileMeta);
        }

        const blob = await fetchFileBlob(id);
        setContentType(blob.type);

        if (blob.type.startsWith('image/')) {
          const url = URL.createObjectURL(blob);
          setContent({ type: 'image', url });
        } else if (blob.type === 'text/plain' || blob.type === 'application/json') {
          const text = await blob.text();
          setContent({ type: 'text', data: text });
        } else {
          setContent({ type: 'unsupported', blob });
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadFileAndContent();

    return () => {
      if (content?.type === 'image' && content.url) {
        URL.revokeObjectURL(content.url);
      }
    };
  }, [id, file]);

  const handleDownload = () => {
    if (file) {
      downloadFile(file.id, file.original_name);
    }
  };

  if (loading) return <p>Loading file...</p>;
  if (error) return (
    <div className="file-detail">
      <button onClick={() => navigate(-1)}>Back</button>
      <p className="error-message">Error: {error}</p>
    </div>
  );

  return (
    <div className="file-detail">
      <button onClick={() => navigate(-1)}>Back</button>
      <h2>{file?.original_name}</h2>
      <p>Type: {file?.mime_type}</p>
      <p>Size: {(file?.size / 1024).toFixed(2)} KB</p>
      <p>Uploaded: {new Date(file?.upload_time).toLocaleString()}</p>

      <div className="content-preview">
        {content?.type === 'image' && (
          <img src={content.url} alt={file.original_name} style={{ maxWidth: '100%' }} />
        )}
        {content?.type === 'text' && (
          <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
            {content.data}
          </pre>
        )}
        {content?.type === 'unsupported' && (
          <p>Preview not available for this file type.</p>
        )}
      </div>

      <button onClick={handleDownload}>Download</button>
    </div>
  );
}