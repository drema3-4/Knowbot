import React, { useRef, useState } from 'react';
import { Button, Card } from 'react-bootstrap';
import UploadStatus from './UploadStatus';
import { uploadFile } from '../services/Upload';
import './FileSelector.css'; // для кастомных стилей

const FileSelector: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [uploadMessage, setUploadMessage] = useState<string>('');

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus('idle');
      setUploadMessage('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setUploadMessage('');

    try {
      const response = await uploadFile(selectedFile);
      setUploadStatus('success');
      setUploadMessage(response.message || 'Файл успешно загружен');
      // Можно оставить файл выбранным или сбросить – решим позже
    } catch (error) {
      setUploadStatus('error');
      setUploadMessage(error instanceof Error ? error.message : 'Неизвестная ошибка');
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setUploadStatus('idle');
    setUploadMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = ''; // очищаем input
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <Card className="file-selector-card">
      <Card.Body>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.zip"
          style={{ display: 'none' }}
        />

        {!selectedFile ? (
          <div
            className="upload-area"
            onClick={openFileDialog}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && openFileDialog()}
          >
            <p className="mb-2">📄 Нажмите для выбора файла</p>
            <p className="text-muted small">Поддерживаются PDF и ZIP</p>
          </div>
        ) : (
          <div className="selected-file-info">
            <p className="mb-2">
              <strong>Выбран файл:</strong> {selectedFile.name}
            </p>
            <div className="d-flex gap-2">
              <Button
                variant="primary"
                onClick={handleUpload}
                disabled={uploadStatus === 'uploading'}
              >
                {uploadStatus === 'uploading' ? 'Загрузка...' : 'Загрузить'}
              </Button>
              <Button variant="outline-secondary" onClick={handleClear}>
                Отмена
              </Button>
            </div>
          </div>
        )}

        <UploadStatus status={uploadStatus} message={uploadMessage} />
      </Card.Body>
    </Card>
  );
};

export default FileSelector;