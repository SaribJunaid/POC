import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { createChat } from '@n8n/chat';
import '@n8n/chat/style.css';
import { useSession } from '../hooks/useSession';

const WEBHOOK_URL = 'https://n8n.irenictech.xyz/webhook/1e8ec14d-2898-4d17-a49f-0c2eb0cfa8f4/chat';

export default function ChatPage() {
  const { locationId } = useParams();
  const { session, loading, error } = useSession();

  useEffect(() => {
    if (!session) {
      return;
    }

    const container = document.getElementById('n8n-chat-root');
    if (!container || container.dataset.initialized === 'true') {
      return;
    }

    container.dataset.initialized = 'true';

    const chatInstance = createChat({
      target: '#n8n-chat-root',
      webhookUrl: WEBHOOK_URL,
      mode: 'window',
      showWelcomeScreen: false,
      loadPreviousSession: true,
      enableStreaming: true,
      metadata: {
        jwt: session.jwt,
        userId: session.userId,
        companyId: session.companyId,
        locationId: session.activeLocation || locationId || '',
        email: session.email,
        userName: session.userName,
        role: session.role,
        conversationId: `${session.companyId}-${session.userId}`,
      },
    });

    return () => {
      container.dataset.initialized = 'false';
      chatInstance?.destroy?.();
    };
  }, [locationId, session]);

  if (loading) {
    return <div className="widget-shell" />;
  }

  if (error || !session) {
    return <div className="widget-shell"><div className="widget-state">Authentication failed</div></div>;
  }

  return <div id="n8n-chat-root" className="widget-shell" />;
}
