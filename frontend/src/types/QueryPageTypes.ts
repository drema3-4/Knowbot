export interface MessageListProps {
    messages: Array<{ id: string; text: string; sender: 'user' | 'bot' }>;
    // messages: Array<{ text: string; sender: 'user' | 'bot' }>;
}

export type Sender = 'user' | 'bot';

export interface MessageProps {
    id: string;
    text: string;
    sender: Sender;
}

export interface MessageBubbleProps {
    id: string;
    text: string;
    sender: Sender;
    className?: string;
}

export interface Message {
    id: string;
    text: string;
    sender: Sender;
}