/**
 * Определяет тип файла по расширению и отправляет его на соответствующий эндпоинт.
 * @param file - выбранный пользователем файл
 * @returns Promise с ответом от сервера (содержит поле message)
 */
export async function uploadFile(file: File): Promise<{ message: string }> {
  const extension = file.name.split('.').pop()?.toLowerCase();

  let url = '';
  if (extension === 'pdf') {
    url = '/api/v1/upload/pdf';
  } else if (extension === 'zip') {
    url = '/api/v1/upload/zip';
  } else {
    return Promise.reject(new Error('Неподдерживаемый тип файла. Ожидается .pdf или .zip'));
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(url, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    // Пытаемся получить текст ошибки от сервера, если есть
    let errorText = 'Ошибка при загрузке файла';
    try {
      const errorData = await response.json();
      errorText = errorData.detail || errorText;
    } catch {
      // игнорируем
    }
    throw new Error(errorText);
  }

  return response.json();
}