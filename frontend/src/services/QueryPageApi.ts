import type { Message } from "../types/QueryPageTypes";

const API_BASE = '/api/v1';


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