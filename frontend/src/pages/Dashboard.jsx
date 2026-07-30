import { useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useSession } from '../hooks/useSession';
import { logout } from '../services/ssoService';

export default function Dashboard() {
  const navigate = useNavigate();
  const { locationId } = useParams();
  const { session, loading, error, logout: clearSession } = useSession();

  const summary = useMemo(() => {
    if (!session) return null;
    return [
      ['User Name', session.userName || 'N/A'],
      ['Email', session.email || 'N/A'],
      ['Role', session.role || 'N/A'],
      ['Company ID', session.companyId || 'N/A'],
      ['User ID', session.userId || 'N/A'],
      ['Location ID', locationId || session.activeLocation || 'N/A'],
      ['Agency Owner', session.isAgencyOwner ? 'Yes' : 'No'],
      ['Type', session.type || 'N/A'],
      ['Version ID', session.versionId || 'N/A'],
      ['App Status', session.appStatus || 'N/A'],
      ['Whitelabel Domain', session.whitelabelDomain || 'N/A'],
      ['Logo URL', session.logoUrl || 'N/A'],
    ];
  }, [locationId, session]);

  if (loading) {
    return (
      <div className="container">
        <div className="card">Loading your session...</div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="container">
        <div className="card">
          <h2>Session unavailable</h2>
          <p>{error || 'Your session could not be loaded.'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
          <div>
            <h1>Dashboard</h1>
            <p>Authenticated through the official GHL Custom Page SSO flow.</p>
          </div>
          <button
            onClick={() => {
              clearSession();
              logout();
              navigate('/', { replace: true });
            }}
            style={{ padding: '0.75rem 1rem', cursor: 'pointer' }}
          >
            Logout
          </button>
        </div>
        <div className="grid two-col" style={{ marginTop: '1rem' }}>
          {summary.map(([label, value]) => (
            <div key={label} className="debug-item">
              <strong>{label}</strong>
              <div>{value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
