import type { Message } from "../types/QueryPageTypes";

const API_BASE = '/api/v1';

/**
 * Отправляет вопрос пользователя и получает ответ бота.
 * @param question - текст вопроса
 * @param userId - ID пользователя
 * @param dialogId - ID диалога (опционально, если не указан, будет создан новый)
 * @returns Promise с сообщением бота
 */
export async function sendMessage(
  question: string,
  userId: number,
  dialogId?: number
): Promise<Message> {
  const response = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      question: question,
      dialog_id: dialogId, // может быть undefined
    }),
  });

  if (!response.ok) {
    let errorText = 'Ошибка при отправке сообщения';
    try {
      const errorData = await response.json();
      errorText = errorData.detail || errorText;
    } catch {
      // игнорируем
    }
    throw new Error(errorText);
  }

  const data = await response.json();
  // data имеет формат QueryResponse: { id: string, text: string, sender: "bot" }
  return {
    id: data.id,
    text: data.text,
    sender: 'bot',
  };
}