import React, { createContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Context to hold JWT and user payload
export const AuthContext = createContext({
  token: null,
  user: null,
  setToken: () => {},
});

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('jwt') || null);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // Decode token payload (base64 part) without verification for UI display
  const decodePayload = (jwt) => {
    try {
      const payload = jwt.split('.')[1];
      const decoded = JSON.parse(atob(payload));
      return decoded;
    } catch (e) {
      return null;
    }
  };

  useEffect(() => {
    if (token) {
      const payload = decodePayload(token);
      setUser(payload);
    } else {
      setUser(null);
    }
  }, [token]);

  // Logout clears storage and redirects to login page
  const logout = () => {
    localStorage.removeItem('jwt');
    setToken(null);
    navigate('/');
  };

  // Persist token changes to localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem('jwt', token);
    }
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, setToken, user, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
