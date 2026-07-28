export default function Authorized({ authResult }) {
  return (
    <div className="card">
      <div className="status-pill authorized">AUTHORIZED</div>
      <h2>GHL Authentication POC</h2>
      <p>Access granted to the current user.</p>
      <div className="grid two-col">
        <div className="debug-item"><strong>User</strong><br />{authResult?.user?.name || 'Unknown'}</div>
        <div className="debug-item"><strong>Email</strong><br />{authResult?.user?.email || 'Unknown'}</div>
        <div className="debug-item"><strong>User ID</strong><br />{authResult?.user?.id || 'Unknown'}</div>
        <div className="debug-item"><strong>Role</strong><br />{authResult?.user?.role || 'Unknown'}</div>
        <div className="debug-item"><strong>Agency Owner</strong><br />{authResult?.user?.isAgencyOwner ? 'Yes' : 'No'}</div>
        <div className="debug-item"><strong>Location</strong><br />{authResult?.location?.name || 'Unknown'}</div>
        <div className="debug-item"><strong>Location ID</strong><br />{authResult?.location?.id || 'Unknown'}</div>
        <div className="debug-item"><strong>Company ID</strong><br />{authResult?.location?.companyId || 'Unknown'}</div>
      </div>
    </div>
  );
}
