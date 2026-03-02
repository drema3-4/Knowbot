const API_BASE = '/api/v1';

export interface User {
  user_id: number;
  user_name: string;
}

/**
 * Создаёт или получает существующего пользователя по имени.
 * POST /api/v1/users с { user_name: name }
 */
export async function createOrGetUser(userName: string): Promise<User> {
  const response = await fetch(`${API_BASE}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_name: userName }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Ошибка при создании пользователя');
  }

  return response.json();
}