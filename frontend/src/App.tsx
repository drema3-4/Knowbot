import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { UserProvider, useUser } from './context/UserContext';
import Navigation from './components/Navigation';
import QueryPage from './pages/QueryPage';
import UploadPage from './pages/UploadPage';
import LoginPage from './pages/LoginPage';
import type { JSX } from 'react';

// Компонент для защиты маршрутов
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { user, isLoading } = useUser();
  if (isLoading) {
    // Можно показать спиннер на весь экран
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Загрузка...</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// Компонент для маршрута логина: если уже залогинен, редирект на главную
const LoginRoute = () => {
  const { user, isLoading } = useUser();
  if (isLoading) return <div>Загрузка...</div>;
  if (user) return <Navigate to="/" replace />;
  return <LoginPage />;
};

function AppContent() {
  return (
    <div
      id="main-container"
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: '100vw',
        height: '100vh',
        margin: 0,
        padding: 0,
        overflow: 'hidden',
      }}
    >
      <Navigation />
      <div style={{ flex: 1, overflow: 'auto' }}>
        <Routes>
          <Route path="/login" element={<LoginRoute />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <QueryPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <UploadPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <UserProvider>
        <AppContent />
      </UserProvider>
    </BrowserRouter>
  );
}

export default App;