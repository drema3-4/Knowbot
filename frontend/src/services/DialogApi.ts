import type { Dialog, BackendMessage, Message } from '../types/QueryPageTypes';

const API_BASE = '/api/v1';

/**
 * Получить все диалоги пользователя
 * GET /dialogs/user/{userId}
 */
export async function fetchUserDialogs(userId: number): Promise<Dialog[]> {
  const response = await fetch(`${API_BASE}/dialogs/user/${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch dialogs');
  }
  return response.json();
}

/**
 * Создать новый диалог для пользователя
 * POST /dialogs с { user_id: userId }
 */
export async function createDialog(userId: number): Promise<Dialog> {
  const response = await fetch(`${API_BASE}/dialogs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId }),
  });
  if (!response.ok) {
    throw new Error('Failed to create dialog');
  }
  return response.json();
}

/**
 * Получить сообщения диалога
 * GET /dialogs/{dialogId}/messages?user_id={userId}
 */
export async function fetchDialogMessages(dialogId: number, userId: number): Promise<Message[]> {
  const url = `${API_BASE}/dialogs/${dialogId}/messages?user_id=${userId}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch messages');
  }
  const backendMessages: BackendMessage[] = await response.json();

  // Преобразуем в формат фронта
  return backendMessages.map(msg => ({
    id: msg.message_id.toString(),
    text: msg.content,
    sender: msg.role === 'user' ? 'user' : 'bot',
  }));
}