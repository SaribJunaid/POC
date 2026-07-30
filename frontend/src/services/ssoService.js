const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const TRUSTED_PARENT_ORIGINS = (import.meta.env.VITE_GHL_PARENT_ORIGINS || '')
  .split(',')
  .map((origin) => origin.trim())
  .filter(Boolean);

function getToken() {
  return sessionStorage.getItem('access_token');
}

function isTrustedParentOrigin(origin) {
  if (!origin || origin === 'null') {
    return false;
  }

  if (TRUSTED_PARENT_ORIGINS.length === 0) {
    try {
      return origin === window.location.origin || /(^|\.)gohighlevel\.com$/.test(new URL(origin).hostname);
    } catch {
      return false;
    }
  }

  return TRUSTED_PARENT_ORIGINS.includes(origin);
}

function extractEncryptedPayload(data) {
  if (!data || data.message !== 'REQUEST_USER_DATA_RESPONSE') {
    return null;
  }

  return data.payload || data.key || data.encryptedPayload || null;
}

export async function requestSSOKey() {
  return new Promise((resolve, reject) => {
    const timeout = window.setTimeout(() => {
      window.removeEventListener('message', listener);
      reject(new Error('SSO response timed out after 10 seconds'));
    }, 10_000);

    const listener = (event) => {
      if (!isTrustedParentOrigin(event.origin)) {
        return;
      }

      const encryptedPayload = extractEncryptedPayload(event.data);
      if (encryptedPayload) {
        window.clearTimeout(timeout);
        window.removeEventListener('message', listener);
        resolve(encryptedPayload);
      }
    };

    window.addEventListener('message', listener);
    window.parent.postMessage({ message: 'REQUEST_USER_DATA' }, '*');
  });
}

export async function validateSSOKey(ssoKey) {
  const response = await fetch(`${API_BASE}/sso/decrypt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key: ssoKey }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'SSO validation failed');
  }

  const data = await response.json();
  sessionStorage.setItem('access_token', data.access_token);
  return data;
}

export async function fetchSession() {
  const token = getToken();
  if (!token) {
    throw new Error('No access token found');
  }

  const response = await fetch(`${API_BASE}/sso/session`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (response.status === 401) {
    sessionStorage.removeItem('access_token');
    throw new Error('Session expired');
  }

  if (!response.ok) {
    throw new Error(`Session fetch failed: ${response.status}`);
  }

  return response.json();
}

export function isAuthenticated() {
  return Boolean(getToken());
}

export function logout() {
  sessionStorage.removeItem('access_token');
}
