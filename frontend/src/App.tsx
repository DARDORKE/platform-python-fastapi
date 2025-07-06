/**
 * Main App component
 */
import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import Layout from './components/Layout/Layout';
import LoginForm from './components/Auth/LoginForm';
import { ToastContainer } from './components/ui/Toast';
import { ConfirmDialogProvider } from './components/ui/ConfirmDialog';

const App: React.FC = () => {
  const { isAuthenticated, user, fetchUser } = useAuthStore();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token && !user) {
      fetchUser().catch(() => {
        // Token is invalid, will be handled by interceptor
      });
    }
  }, [user, fetchUser]);

  return (
    <ConfirmDialogProvider>
      <Router>
        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ? <Navigate to="/" replace /> : <LoginForm />
            }
          />
          <Route
            path="/*"
            element={
              isAuthenticated ? (
                <Layout />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
        </Routes>
        <ToastContainer />
      </Router>
    </ConfirmDialogProvider>
  );
};

export default App;