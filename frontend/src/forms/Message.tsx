import MessageBubble from './MessageBubble';
import type { MessageProps } from '../types/QueryPageTypes';


function Message({ id, text, sender } : MessageProps) {
    return (
        <div
            className={`d-flex ${
            sender === 'user' ? 'justify-content-end' : 'justify-content-start'
            } mb-2`}
        >
            <div style={{ maxWidth: '70%' }}>
                <MessageBubble id={id} text={text} sender={sender} />
            </div>
        </div>
    );
}

export default Message;