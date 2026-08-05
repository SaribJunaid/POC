export default function ChatInput({ value, onChange, onSend, disabled }) {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSend();
    }
  };

  return (
    <div className="chat-input-wrapper">
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        rows={2}
        className="chat-textarea"
        disabled={disabled}
      />
      <button className="chat-send-button" onClick={onSend} disabled={disabled || !value.trim()}>
        Send
      </button>
    </div>
  );
}
