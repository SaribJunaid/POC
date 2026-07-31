import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../services/ssoService";

export default function ProtectedRoute({ children }) {
    if (!isAuthenticated()) {
        return <Navigate to="/" replace />;
    }

    return children;
}