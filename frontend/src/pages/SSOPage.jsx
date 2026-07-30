import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Loading from '../components/Loading';
import { fetchSession, requestSSOKey, validateSSOKey } from '../services/ssoService';

export default function SSOPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState('Requesting SSO payload from GHL...');
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;

    const init = async () => {
      try {
        setStatus('Requesting SSO payload from GHL...');
        const ssoKey = await requestSSOKey();

        setStatus('Validating SSO payload with backend...');
        await validateSSOKey(ssoKey);

        setStatus('Loading your session...');
        const session = await fetchSession();
        if (!active) return;

        const activeLocation = session?.data?.activeLocation || session?.activeLocation;
        const target = activeLocation ? `/location/${activeLocation}` : '/dashboard';
        navigate(target, { replace: true });
      } catch (err) {
        if (!active) return;
        setError(err.message || 'SSO failed');
      }
    };

    init();
    return () => {
      active = false;
    };
  }, [navigate]);

  if (error) {
    return (
      <div className="container">
        <div className="card" style={{ textAlign: 'center' }}>
          <h2>Authentication failed</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return <Loading />;
}
