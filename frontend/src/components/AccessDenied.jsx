export default function AccessDenied({ user, location }) {
  return (
    <div className="card">
      <div className="status-pill denied">ACCESS DENIED</div>
      <h2>You do not have permission to access this application.</h2>
      <div className="grid two-col">
        <div className="debug-item"><strong>User</strong><br />{user?.name || 'Unknown'}</div>
        <div className="debug-item"><strong>Email</strong><br />{user?.email || 'Unknown'}</div>
        <div className="debug-item"><strong>Role</strong><br />{user?.role || 'Unknown'}</div>
        <div className="debug-item"><strong>Location</strong><br />{location?.name || 'Unknown'}</div>
      </div>
    </div>
  );
}
