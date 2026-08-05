import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useSession } from '../hooks/useSession';
import { sendMessage } from '../services/chatService';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';

function buildUserPayload(session) {
  return {
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
}

export default function ChatPage() {
  const navigate = useNavigate();
  const { locationId } = useParams();
  const { session, loading, error, logout: clearSession } = useSession();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [sendError, setSendError] = useState(null);
  const messageEndRef = useRef(null);

  const userName = session?.userName || session?.email || 'You';
  const userMeta = useMemo(() => buildUserPayload(session), [session]);

  useEffect(() => {
    if (session) {
      setMessages((current) => {
        if (current.length > 0) return current;
        return [
          {
            id: 'welcome',
            role: 'assistant',
            content: `Welcome back, ${userName}! Ask me anything about your GoHighLevel environment.`,
            timestamp: new Date().toISOString(),
          },
        ];
      });
    }
  }, [session, userName]);

  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages, isSending]);

  const handleLogout = () => {
    clearSession();
    navigate('/', { replace: true });
  };

  const handleSend = async () => {
    const trimmedMessage = inputValue.trim();
    if (!trimmedMessage || !session || isSending) {
      return;
    }

    setSendError(null);

    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: trimmedMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((current) => [...current, userMessage]);
    setInputValue('');
    setIsSending(true);

    try {
      const reply = await sendMessage(trimmedMessage, userMeta);
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: reply || 'No response received from the assistant.',
        timestamp: new Date().toISOString(),
      };
      setMessages((current) => [...current, assistantMessage]);
    } catch (sendErr) {
      setSendError(sendErr.message || 'Unable to reach AI assistant. Please try again.');
      const errorMessage = {
        id: `assistant-error-${Date.now()}`,
        role: 'assistant',
        content: 'Unable to reach AI assistant. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((current) => [...current, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

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
          <button onClick={handleLogout}>Back to sign in</button>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-page-container">
      <div className="chat-shell">
        <header className="chat-header">
          <div>
            <p className="chat-label">GoHighLevel AI Assistant</p>
            <h1 className="chat-title">Hi {userName}.</h1>
            <p className="chat-subtitle">Authenticated as {session.role || 'member'}{locationId ? ` · Location ${locationId}` : ''}</p>
          </div>
          <div className="chat-actions">
            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        <section className="chat-body">
          <ChatWindow messages={messages} isTyping={isSending} />
          <div ref={messageEndRef} />
        </section>

        <div className="chat-footer">
          {sendError && <div className="chat-error">{sendError}</div>}
          <ChatInput value={inputValue} onChange={setInputValue} onSend={handleSend} disabled={isSending} />
        </div>
      </div>
    </div>
  );
}
