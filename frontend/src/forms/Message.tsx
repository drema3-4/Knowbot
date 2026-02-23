import MessageBubble from './MessageBubble';

interface MessageProps {
  text: string;
  sender: 'user' | 'bot';
  // Дополнительные пропсы, например, timestamp, можно добавить позже
}

const Message: React.FC<MessageProps> = ({ text, sender }) => {
  return (
    <div
      className={`d-flex ${
        sender === 'user' ? 'justify-content-end' : 'justify-content-start'
      } mb-2`}
    >
      {/* Можно добавить аватар слева для бота, если нужно, но пока нет */}
      <div style={{ maxWidth: '70%' }}>
        <MessageBubble text={text} sender={sender} />
      </div>
      {/* Можно добавить аватар справа для пользователя */}
    </div>
  );
};

export default Message;