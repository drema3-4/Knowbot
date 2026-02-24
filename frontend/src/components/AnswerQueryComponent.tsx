import Message from '../forms/Message';
import type { MessageListProps } from '../types/QueryPageTypes';


function AnswerQueryComponent({ messages } : MessageListProps) {
    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ width: '100%', maxWidth: '800px', height: '100%', overflowY: 'auto', padding: '1rem' }}>
                {messages.map((msg) => (
                    <Message key={msg.id} text={msg.text} sender={msg.sender} />
                ))}
            </div>
        </div>
    );
}

export default AnswerQueryComponent;