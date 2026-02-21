import { useState } from 'react';
import FileRow from './FileRow';
import { downloadFile } from '../services/api';

export default function FileList({ files, onFileSelect, selectedFiles, onDownloadSelected }) {
  const handleSelectAll = (e) => {
    const checked = e.target.checked;
    files.forEach(file => {
      onFileSelect(file.id, checked);
    });
  };

  const handleDownloadSelected = () => {
    selectedFiles.forEach(fileId => {
      const file = files.find(f => f.id === fileId);
      if (file) downloadFile(file.id, file.original_name);
    });
  };

  const allSelected = files.length > 0 && files.every(file => selectedFiles.includes(file.id));

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>
              <input
                type="checkbox"
                checked={allSelected}
                onChange={handleSelectAll}
              />
            </th>
            <th>Name</th>
            <th>Size</th>
            <th>Type</th>
            <th>Uploaded</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {files.map(file => (
            <FileRow
              key={file.id}
              file={file}
              isSelected={selectedFiles.includes(file.id)}
              onSelect={onFileSelect}
            />
          ))}
        </tbody>
      </table>
      {selectedFiles.length > 0 && (
        <button onClick={handleDownloadSelected}>
          Download Selected ({selectedFiles.length})
        </button>
      )}
    </div>
  );
}