import { useEffect, useState } from 'react';
import { fetchSession, isAuthenticated, logout } from '../services/ssoService';

export function useSession() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      if (!isAuthenticated()) {
        setLoading(false);
        return;
      }

      try {
        const data = await fetchSession();
        setSession(data?.data || data || null);
      } catch (err) {
        setError(err.message || 'Session error');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { session, loading, error, logout: () => { logout(); setSession(null); } };
}
