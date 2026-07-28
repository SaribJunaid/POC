const DEFAULT_TRUSTED_ORIGINS = ['http://localhost:5173', 'https://localhost:5173'];

function getQueryParams(search = window.location.search) {
  const params = new URLSearchParams(search);
  return Object.fromEntries(params.entries());
}

function getHashParams(hash = window.location.hash) {
  const params = new URLSearchParams(hash.startsWith('#') ? hash.slice(1) : hash);
  return Object.fromEntries(params.entries());
}

export function discoverGhlContext(trustedOrigins = DEFAULT_TRUSTED_ORIGINS) {
  const queryParams = getQueryParams();
  const hashParams = getHashParams();
  const combined = { ...queryParams, ...hashParams };

  const locationId = combined.locationId || combined.location_id || null;
  const userId = combined.userId || combined.user_id || null;
  const email = combined.email || null;

  const result = {
    locationId,
    userId,
    email,
    source: null,
    rawContext: {},
  };

  const preferUrl = (key, value) => {
    if (value && !result[key]) {
      result[key] = value;
      result.source = 'url';
    }
  };

  preferUrl('locationId', locationId);
  preferUrl('userId', userId);
  preferUrl('email', email);

  if (typeof window !== 'undefined') {
    const globalContext = window.__GHL_CONTEXT__ || window.ghlContext || null;
    if (globalContext) {
      result.locationId = result.locationId || globalContext.locationId || globalContext.location_id || null;
      result.userId = result.userId || globalContext.userId || globalContext.user_id || null;
      result.email = result.email || globalContext.email || null;
      result.source = result.source || 'window';
      result.rawContext = globalContext;
    }
  }

  const state = typeof window !== 'undefined' ? (window.__GHL_POST_MESSAGE_STATE__ || { postMessagesReceived: [] }) : { postMessagesReceived: [] };
  const receiveMessage = (event) => {
    const originAllowed = trustedOrigins.includes(event.origin);
    if (!originAllowed) {
      return;
    }
    const payload = event.data && typeof event.data === 'object' ? event.data : { value: event.data };
    state.postMessagesReceived.push({ origin: event.origin, data: payload });
    if (payload.locationId || payload.location_id) {
      result.locationId = result.locationId || payload.locationId || payload.location_id || null;
    }
    if (payload.userId || payload.user_id) {
      result.userId = result.userId || payload.userId || payload.user_id || null;
    }
    if (payload.email) {
      result.email = result.email || payload.email || null;
    }
    result.source = 'postMessage';
    if (typeof window !== 'undefined') {
      window.__GHL_POST_MESSAGE_STATE__ = state;
    }
  };

  if (typeof window !== 'undefined') {
    window.addEventListener('message', receiveMessage);
    window.__GHL_POST_MESSAGE_STATE__ = state;
  }

  return {
    ...result,
    isIframe: typeof window !== 'undefined' && window.self !== window.top,
    currentUrl: typeof window !== 'undefined' ? window.location.href : '',
    queryParams,
    hashParams,
    postMessagesReceived: state.postMessagesReceived,
    cleanup: () => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('message', receiveMessage);
      }
    },
  };
}
