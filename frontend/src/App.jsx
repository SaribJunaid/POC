import { BrowserRouter, Route, Routes } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import SSOPage from './pages/SSOPage';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SSOPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/location/:locationId"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}