import type { Message } from "../types/QueryPageTypes";

const API_BASE = '/api/v1';

// export async function fetchHistory(): Promise<Message[]> {
//     const res = await fetch(`${API_BASE}/history`);
//     if (!res.ok) throw new Error('Failed to load history');
//     const data = await res.json();
//     return data.messages; // предполагаем, что сервер возвращает { messages: [...] }
// }

export async function sendMessage(question: string): Promise<Message> {
    const res = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question }),
    });
    if (!res.ok) throw new Error('Failed to send message');
    const message = await res.json();
    return message; // сервер возвращает { message: { id, role, content, timestamp } }
}

// export async function sendMessage(question: string): Promise<Message> {
//     console.log('📤 Отправка вопроса:', question);  // ← добавить

//     const response = await fetch(`${API_BASE}/query`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ question }),
//     });

//     if (!response.ok) {
//         const error = await response.text();
//         console.error('❌ Ошибка ответа:', error);    // ← добавить
//         throw new Error(error);
//     }

//     const data = await response.json();
//     console.log('📥 Получен ответ:', data);         // ← добавить
//     return data.message;
// }