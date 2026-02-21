import { useNavigate } from 'react-router-dom';
import { downloadFile } from '../services/api';

export default function FileRow({ file, isSelected, onSelect, onDownload }) {
  const navigate = useNavigate();

  const handleDownload = (e) => {
    e.stopPropagation();
    downloadFile(file.id, file.original_name);
  };

  const handleRowClick = () => {
    navigate(`/file/${file.id}`, { state: { file } });
  };

  return (
    <tr onClick={handleRowClick} style={{ cursor: 'pointer' }}>
      <td onClick={(e) => e.stopPropagation()}>
        <input
          type="checkbox"
          checked={isSelected}
          onChange={(e) => onSelect(file.id, e.target.checked)}
        />
      </td>
      <td>{file.original_name}</td>
      <td>{(file.size / 1024).toFixed(2)} KB</td>
      <td>{file.mime_type}</td>
      <td>{new Date(file.upload_time).toLocaleString()}</td>
      <td onClick={(e) => e.stopPropagation()}>
        <button onClick={handleDownload}>Download</button>
      </td>
    </tr>
  );
}