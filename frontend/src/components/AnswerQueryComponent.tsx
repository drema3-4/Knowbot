import React from 'react';
import Message from '../forms/Message';

interface MessageListProps {
  messages: Array<{ id: string; text: string; sender: 'user' | 'bot' }>;
}

const AnswerQueryComponent: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="p-3 overflow-auto" style={{ height: '100%' }}>
      {messages.map((msg) => (
        <Message key={msg.id} text={msg.text} sender={msg.sender} />
      ))}
    </div>
  );
};

export default AnswerQueryComponent;