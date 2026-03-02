export interface MessageListProps {
    messages: Array<{ id: string; text: string; sender: 'user' | 'bot' }>;
    // messages: Array<{ text: string; sender: 'user' | 'bot' }>;
}

export type Sender = 'user' | 'bot';

export interface MessageProps {
    text: string;
    sender: Sender;
}

export interface MessageBubbleProps {
    text: string;
    sender: Sender;
    className?: string;
}

export interface Message {
    id: string;          // строковый ID для удобства (можно и число)
    text: string;
    sender: 'user' | 'bot';
    // можно добавить timestamp?: string
}

export interface Dialog {
    dialog_id: number;
    user_id: number;
    created_at: string; // или Date, но пока string
}

// Для ответа от бэкенда по сообщениям (если нужен маппинг)
export interface BackendMessage {
    message_id: number;
    user_id: number;
    dialog_id: number;
    role: string;        // 'user' или 'assistant'
    content: string;
    created_at: string;
}