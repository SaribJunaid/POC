const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Request failed');
  }

  return response.json();
}

export async function healthCheck() {
  return request('/health');
}

export async function getGhlContext(locationId) {
  return request(`/api/ghl/context?location_id=${encodeURIComponent(locationId)}`);
}

export async function validateAuth(payload) {
  return request('/api/auth/validate', { method: 'POST', body: JSON.stringify(payload) });
}

export async function getConfig() {
  return request('/api/config');
}
