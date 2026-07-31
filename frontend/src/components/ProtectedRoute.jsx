import { Navigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const { token } = useContext(AuthContext);
  // If no JWT token present, user is not authenticated
  if (!token) {
    return <Navigate to="/" replace state={{ from: location }} />;
  }

  return children;
}
