import MessageBubble from './MessageBubble';

export default function ChatWindow({ messages, isTyping }) {
  return (
    <div className="chat-window">
      {messages.map((message) => (
        <MessageBubble key={message.id} role={message.role} content={message.content} timestamp={message.timestamp} />
      ))}
      {isTyping && (
        <div className="message-row message-row-assistant">
          <div className="message-bubble message-bubble-assistant typing-bubble">
            <div className="typing-dots">
              <span />
              <span />
              <span />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
