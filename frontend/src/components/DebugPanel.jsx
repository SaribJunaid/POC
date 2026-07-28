export default function DebugPanel({ debug }) {
  const copyDebugData = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(debug, null, 2));
      alert('Debug data copied to clipboard.');
    } catch (error) {
      console.error('Failed to copy debug data', error);
    }
  };

  return (
    <div className="card" style={{ marginTop: '1rem' }}>
      <h3>Debug Panel</h3>
      <button onClick={copyDebugData} style={{ marginBottom: '1rem' }}>Copy Debug Data</button>
      <div className="debug-list">
        <div className="debug-item"><strong>Current URL</strong><br />{debug.currentUrl}</div>
        <div className="debug-item"><strong>Query Params</strong><br /><pre>{JSON.stringify(debug.queryParams, null, 2)}</pre></div>
        <div className="debug-item"><strong>Hash Params</strong><br /><pre>{JSON.stringify(debug.hashParams, null, 2)}</pre></div>
        <div className="debug-item"><strong>Detected Location ID</strong><br />{debug.locationId || 'None'}</div>
        <div className="debug-item"><strong>Detected User ID</strong><br />{debug.userId || 'None'}</div>
        <div className="debug-item"><strong>Detected Email</strong><br />{debug.email || 'None'}</div>
        <div className="debug-item"><strong>Identity Source</strong><br />{debug.identitySource || 'None'}</div>
        <div className="debug-item"><strong>Is Iframe</strong><br />{String(debug.isIframe)}</div>
        <div className="debug-item"><strong>Parent Window Available</strong><br />{String(debug.parentWindowAvailable)}</div>
        <div className="debug-item"><strong>Received postMessage Events</strong><br /><pre>{JSON.stringify(debug.postMessagesReceived, null, 2)}</pre></div>
      </div>
    </div>
  );
}
