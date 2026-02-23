import React from 'react';
import Message from '../forms/Message';

interface MessageListProps {
  messages: Array<{ id: string; text: string; sender: 'user' | 'bot' }>;
}

const AnswerQueryComponent: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ width: '100%', maxWidth: '800px', height: '100%', overflowY: 'auto', padding: '1rem' }}>
        {messages.map((msg) => (
          <Message key={msg.id} text={msg.text} sender={msg.sender} />
        ))}
      </div>
    </div>
  );
};

export default AnswerQueryComponent;