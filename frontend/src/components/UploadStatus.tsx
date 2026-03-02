import React from 'react';
import { Alert, Spinner } from 'react-bootstrap';

interface UploadStatusProps {
  status: 'idle' | 'uploading' | 'success' | 'error';
  message?: string;
}

const UploadStatus: React.FC<UploadStatusProps> = ({ status, message }) => {
  if (status === 'idle') {
    return null;
  }

  if (status === 'uploading') {
    return (
      <div className="d-flex align-items-center mt-3">
        <Spinner animation="border" size="sm" variant="primary" className="me-2" />
        <span className="text-muted">Загрузка файла, пожалуйста, подождите...</span>
      </div>
    );
  }

  if (status === 'success') {
    return (
      <Alert variant="success" className="mt-3">
        {message || 'Файл успешно загружен и будет обработан в фоновом режиме.'}
      </Alert>
    );
  }

  if (status === 'error') {
    return (
      <Alert variant="danger" className="mt-3">
        {message || 'Произошла ошибка при загрузке файла.'}
      </Alert>
    );
  }

  return null;
};

export default UploadStatus;