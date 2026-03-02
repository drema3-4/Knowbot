import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Card, Alert } from 'react-bootstrap';
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const [userName, setUserName] = useState('');
  const [error, setError] = useState('');
  const { login, isLoading } = useUser();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userName.trim()) {
      setError('Введите имя пользователя');
      return;
    }
    setError('');
    try {
      await login(userName.trim());
      navigate('/'); // после успешного входа переходим на главную (чат)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Неизвестная ошибка');
    }
  };

  return (
    <Container
      fluid
      className="d-flex align-items-center justify-content-center"
      style={{ height: '100%' }}
    >
      <Row className="w-100">
        <Col md={{ span: 6, offset: 3 }} lg={{ span: 4, offset: 4 }}>
          <Card className="shadow">
            <Card.Body>
              <h2 className="text-center mb-4">Вход в Knowbot</h2>
              <p className="text-center text-muted mb-4">
                Введите ваш никнейм для начала работы
              </p>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="userName">
                  <Form.Label>Никнейм</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Введите ник"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    disabled={isLoading}
                    autoFocus
                  />
                </Form.Group>
                {error && <Alert variant="danger">{error}</Alert>}
                <Button
                  variant="primary"
                  type="submit"
                  className="w-100"
                  disabled={isLoading}
                >
                  {isLoading ? 'Вход...' : 'Войти'}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;