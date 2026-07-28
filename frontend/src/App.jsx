import { useEffect, useMemo, useState } from 'react';
import LoadingScreen from './components/LoadingScreen';
import AccessDenied from './components/AccessDenied';
import Authorized from './components/Authorized';
import DebugPanel from './components/DebugPanel';
import { getConfig, getGhlContext, healthCheck, validateAuth } from './services/api';
import { discoverGhlContext } from './utils/ghlContext';

export default function App() {
  const [status, setStatus] = useState('loading');
  const [authResult, setAuthResult] = useState(null);
  const [context, setContext] = useState(null);
  const [error, setError] = useState(null);
  const [debug, setDebug] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const run = async () => {
      try {
        await healthCheck();
        const config = await getConfig();
        const discovered = discoverGhlContext(config.trustedOrigins || []);
        const resolvedDebug = {
          ...discovered,
          identitySource: discovered.locationId || discovered.userId || discovered.email ? discovered.source || 'url' : 'none',
          parentWindowAvailable: typeof window !== 'undefined' && window.parent && window.parent !== window,
          postMessagesReceived: discovered.postMessagesReceived || [],
          currentUrl: discovered.currentUrl,
          queryParams: discovered.queryParams,
          hashParams: discovered.hashParams,
        };

        if (isMounted) {
          setDebug(resolvedDebug);
        }

        if (!discovered.locationId) {
          if (isMounted) {
            setStatus('identity-not-found');
            setContext(null);
          }
          return;
        }

        const ctx = await getGhlContext(discovered.locationId);
        if (isMounted) {
          setContext(ctx);
        }

        if (!discovered.userId && !discovered.email) {
          if (isMounted) {
            setStatus('identity-not-found');
          }
          return;
        }

        const authPayload = {
          location_id: discovered.locationId,
          user_id: discovered.userId || null,
          email: discovered.email || null,
        };

        const result = await validateAuth(authPayload);
        if (isMounted) {
          setAuthResult(result);
          if (result.authorized) {
            setStatus('authorized');
          } else {
            setStatus('denied');
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || 'Unexpected error');
          setStatus('error');
        }
      }
    };

    run();

    return () => {
      isMounted = false;
    };
  }, []);

  const renderContent = useMemo(() => {
    if (status === 'loading') {
      return <LoadingScreen />;
    }
    if (status === 'authorized') {
      return <Authorized authResult={authResult} />;
    }
    if (status === 'denied') {
      return <AccessDenied user={authResult?.user} location={authResult?.location} />;
    }
    if (status === 'identity-not-found') {
      return (
        <div className="card">
          <div className="status-pill info">IDENTITY NOT FOUND</div>
          <h2>GHL Location Detected</h2>
          <p>Location ID: {context?.locationId || debug?.locationId || 'Unknown'}</p>
          <p>Current user identity could not be automatically detected. The POC is unable to determine the current GHL user.</p>
        </div>
      );
    }

    return (
      <div className="card">
        <div className="status-pill denied">GHL API ERROR</div>
        <h2>Unable to complete the POC flow.</h2>
        <p>{error || 'An unexpected error occurred.'}</p>
      </div>
    );
  }, [authResult, context, debug, error, status]);

  return (
    <div className="container">
      <h1>GoHighLevel Authentication POC</h1>
      <p>This demo verifies whether a GHL custom menu link can open an external app and authorize the current user.</p>
      {renderContent}
      {debug && <DebugPanel debug={debug} />}
    </div>
  );
}
