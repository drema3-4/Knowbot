import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import FileSelector from '../components/FileSelector';

const UploadPage: React.FC = () => {
  return (
    <Container
      fluid
      className="d-flex align-items-center justify-content-center"
      style={{ height: '100%' }}
    >
      <Row className="w-100">
        <Col md={{ span: 6, offset: 3 }} lg={{ span: 4, offset: 4 }}>
          <h2 className="text-center mb-4">Загрузка документов</h2>
          <p className="text-center text-muted mb-4">
            Загрузите PDF-файлы или ZIP-архив с PDF. После загрузки документы будут обработаны и добавлены в базу знаний.
          </p>
          <FileSelector />
        </Col>
      </Row>
    </Container>
  );
};

export default UploadPage;