function getConversationId() {
  let conversationId = localStorage.getItem('conversationId');

  if (!conversationId) {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
      conversationId = crypto.randomUUID();
      localStorage.setItem('conversationId', conversationId);
    } else {
      conversationId = `conversation-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
      localStorage.setItem('conversationId', conversationId);
    }
  }

  return conversationId;
}

export async function sendMessage(message, session) {
  const conversationId = getConversationId();
  const timestamp = new Date().toISOString();

  const user = {
    userId: session?.userId ?? '',
    companyId: session?.companyId ?? '',
    email: session?.email ?? '',
    userName: session?.userName ?? '',
    role: session?.role ?? '',
    type: session?.type ?? '',
    activeLocation: session?.activeLocation ?? '',
    isAgencyOwner: Boolean(session?.isAgencyOwner),
    versionId: session?.versionId ?? '',
    appStatus: session?.appStatus ?? '',
    whitelabelDomain: session?.whitelabelDomain ?? '',
    logoUrl: session?.logoUrl ?? '',
  };

  const payload = {
    message,
    conversationId,
    timestamp,
    user,
  };

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000);

    const response = await fetch(
      'https://n8n.irenictech.xyz/webhook/e289fa43-de51-4821-b45b-9a0e8a3867bd',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      }
    );

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error('Unable to reach AI assistant. Please try again.');
    }

    const text = await response.text();
    if (!text.trim()) {
      return '';
    }

    try {
      const data = JSON.parse(text);
      return data?.reply || data?.response || text;
    } catch {
      return text;
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('AI assistant took too long to respond. Please try again.');
    }
    throw new Error(error?.message || 'Unable to reach AI assistant. Please try again.');
  }
}
