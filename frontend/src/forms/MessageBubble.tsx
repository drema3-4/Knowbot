interface MessageBubbleProps {
  text: string;
  sender: 'user' | 'bot';
  className?: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ text, sender, className }) => {
  // Определяем классы Bootstrap в зависимости от отправителя
  const bubbleClasses = `
    p-3
    rounded-3
    ${sender === 'user' ? 'bg-primary text-white' : 'bg-light'}
    ${className || ''}
  `;

  return (
    <div className={bubbleClasses}>
      {text}
    </div>
  );
};

export default MessageBubble;