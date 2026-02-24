import type { Message } from "../types/QueryPageTypes";

const API_BASE = '/api/chat';

export async function fetchHistory(): Promise<Message[]> {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) throw new Error('Failed to load history');
    const data = await res.json();
    return data.messages; // предполагаем, что сервер возвращает { messages: [...] }
}

export async function sendMessage(prompt: string): Promise<Message> {
    const res = await fetch(`${API_BASE}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
    });
    if (!res.ok) throw new Error('Failed to send message');
    const data = await res.json();
    return data.message; // сервер возвращает { message: { id, role, content, timestamp } }
}