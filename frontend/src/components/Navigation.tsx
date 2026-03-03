import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useUser } from '../context/UserContext';

const Navigation: React.FC = () => {
  const { user, logout } = useUser();

  return (
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <Navbar.Brand as={Link} to="/">
          🤖 Knowbot
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              Чат
            </Nav.Link>
            <Nav.Link as={Link} to="/upload">
              Загрузка документов
            </Nav.Link>
          </Nav>
          {user && (
            <Nav>
              <Navbar.Text>
                {user.user_name}{' '}
                <Button
                  variant="link"
                  onClick={logout}
                  style={{ padding: 0 }}
                >
                  Выйти
                </Button>
              </Navbar.Text>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;