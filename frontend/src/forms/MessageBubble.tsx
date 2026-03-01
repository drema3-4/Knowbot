import type { MessageBubbleProps } from "../types/QueryPageTypes";


function MessageBubble({ text, sender, className }: MessageBubbleProps) {
    const bubbleClasses = `
        p-3
        rounded-3
        ${sender === 'user' ? 'bg-primary text-white' : 'bg-light'}
        ${className || ''}
    `;

    return (
        <div className={bubbleClasses}>
            {}{text}
        </div>
    );
}

export default MessageBubble;