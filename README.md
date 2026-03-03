# 🤖 Knowbot

**Knowbot** — это интеллектуальный помощник для ответов на вопросы по технической документации. Проект реализован на основе подхода RAG (Retrieval-Augmented Generation) и позволяет загружать PDF‑файлы, после чего задавать вопросы по их содержимому. Система сохраняет историю диалогов, поддерживает нескольких пользователей и работает через удобный веб‑интерфейс.

---

## 🚀 Возможности

- Загрузка документов в формате PDF (по одному или архивом ZIP)
- Автоматическое извлечение текста, разбиение на фрагменты (chunking) и векторизация
- Ответы на вопросы с использованием языковой модели (LLM) и поиска по векторной базе данных
- Управление пользователями (автоматическое создание при первом входе)
- Сохранение истории диалогов в PostgreSQL
- Веб‑интерфейс на React (TypeScript) с адаптивным дизайном
- Полная контейнеризация через Docker Compose

---

## 🧱 Технологический стек

| Компонент       | Технологии                                                                 |
|----------------|----------------------------------------------------------------------------|
| Бэкенд         | Python 3.12, FastAPI, SQLAlchemy (asyncpg), LangChain, ChromaDB, Uvicorn |
| Фронтенд       | React 19, TypeScript, Vite, React Bootstrap, React Router DOM             |
| База данных    | PostgreSQL 15 (Alpine)                                                     |
| Векторное хранилище | Chroma (с HuggingFaceEmbeddings)                                      |
| Языковая модель | Open‑source / OpenAI‑совместимая (через VseGPT)                          |
| Инфраструктура | Docker, Docker Compose, Nginx (reverse proxy)                             |

---

## 🏗️ Архитектура

Система состоит из четырёх основных сервисов:

1. **Nginx** — выступает в роли reverse‑proxy, обслуживает статику фронтенда и перенаправляет API‑запросы к бэкенду.
2. **Frontend** — React‑приложение, отдаваемое как статика.
3. **Backend** — FastAPI‑приложение, реализующее:
   - эндпоинты для работы с пользователями, диалогами и сообщениями;
   - загрузку и обработку документов (PDF/ZIP);
   - интеграцию с векторным хранилищем (Chroma) и LLM.
4. **PostgreSQL** — реляционная база данных для хранения пользователей, диалогов и сообщений.

При старте бэкенд автоматически создаёт необходимые таблицы в БД и загружает все PDF‑файлы из папки `documents` в векторное хранилище.

---

## 📋 Предварительные требования

- [Docker](https://docs.docker.com/get-docker/) версии 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) версии 2.0+
- (Опционально) Node.js 18+ и pnpm/npm для разработки без Docker

---

## ⚙️ Переменные окружения

Перед запуском необходимо создать файл `.env` в корне проекта (рядом с `docker-compose.yml`). Пример содержимого:

```env
# PostgreSQL
POSTGRES_USER=knowbot_user
POSTGRES_PASSWORD=strong_password
POSTGRES_DB=knowbot_db

# LLM (пример для VseGPT)
LLM_API_KEY=your_api_key_here
LLM_MODEL=openai/gpt-4o-mini
LLM_BASE_URL=https://api.vsegpt.ru/v1
LLM_TEMPERATURE=0.1
```

Все настройки модели, векторизации и текстового сплиттера находятся в `backend/core/config.py` и могут быть изменены без пересборки контейнеров (только через переменные окружения, описанные в `Settings`).

---

## 🐳 Запуск проекта (Docker Compose)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/knowbot.git
   cd knowbot
   ```

2. Создайте файл `.env` с необходимыми переменными (см. выше).

3. Поместите ваши PDF‑документы в папку `backend/documents/` (если папки нет, она будет создана автоматически). При первом запуске все PDF оттуда загрузятся в векторную базу.

4. Запустите контейнеры:
   ```bash
   docker-compose up -d
   ```

5. Откройте браузер и перейдите по адресу `http://localhost`.

   - Фронтенд доступен сразу.
   - API эндпоинты: `http://localhost/api/v1/...`

Для остановки: `docker-compose down`

---

## 💻 Разработка без Docker

### Бэкенд

1. Перейдите в директорию `backend`:
   ```bash
   cd backend
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   pip install -r requirements.txt
   ```

3. Создайте `.env` файл в `backend/` со следующими переменными (пример для локальной БД):
   ```env
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   POSTGRES_DB=...
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   LLM_API_KEY=...
   ```

4. Убедитесь, что PostgreSQL запущен локально (или измените `POSTGRES_HOST` на адрес вашего сервера).

5. Запустите сервер:
   ```bash
   uvicorn api.main:app --reload
   ```

   API будет доступен по адресу `http://localhost:8000`.

### Фронтенд

1. Перейдите в директорию `frontend`:
   ```bash
   cd frontend
   ```

2. Установите зависимости:
   ```bash
   npm install  # или pnpm install
   ```

3. Запустите dev‑сервер:
   ```bash
   npm run dev
   ```

   Приложение будет доступно на `http://localhost:5173`. API‑запросы проксируются на `http://localhost:8000` (настройка в `vite.config.ts`).

---

## 📚 API Эндпоинты

Все эндпоинты имеют префикс `/api/v1`.

### Пользователи

- `POST /users` — создать или получить существующего пользователя по имени.  
  Тело запроса: `{ "user_name": "string" }`  
  Ответ: `{ "user_id": int, "user_name": "string" }`

- `GET /users/by-name/{user_name}` — получить пользователя по имени.

### Диалоги

- `GET /dialogs/user/{user_id}` — получить все диалоги пользователя (отсортированы по убыванию даты создания).
- `POST /dialogs` — создать новый диалог.  
  Тело: `{ "user_id": int }`  
  Ответ: объект диалога с `dialog_id`, `user_id`, `created_at`.

- `GET /dialogs/{dialog_id}/messages?user_id={user_id}` — получить сообщения диалога.

### Сообщения и запросы

- `POST /query` — задать вопрос.  
  Тело: `{ "user_id": int, "question": "string", "dialog_id": int (опционально) }`  
  Если `dialog_id` не указан, создаётся новый диалог.  
  Ответ: `{ "id": "string", "text": "string", "sender": "bot" }`

### Загрузка документов

- `POST /upload/pdf` — загрузить один PDF‑файл (multipart/form-data, поле `file`).
- `POST /upload/zip` — загрузить ZIP‑архив с PDF‑файлами.

Оба эндпоинта запускают фоновую обработку и сразу возвращают `{ "message": "..." }`.

---

## 📁 Структура проекта

```
knowbot/
├── backend/                 # Бэкенд на FastAPI
│   ├── api/                 # Маршруты, зависимости, main.py
│   ├── core/                # Конфигурация, промпты
│   ├── db/                  # Модели, репозитории, сессия SQLAlchemy
│   ├── schemas/             # Pydantic-схемы
│   ├── services/            # DocumentProcessor, RAGEngine, VectorStore...
│   ├── utils/               # Вспомогательные функции для загрузки
│   ├── chroma_db/           # Персистентная директория Chroma (создаётся автоматически)
│   ├── documents/           # Сюда помещаются PDF для автозагрузки
│   ├── upload_tmp_dir/      # Временная папка для распаковки ZIP
│   ├── .env                 # Переменные окружения (не в репозитории)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Фронтенд на React + TypeScript
│   ├── src/
│   │   ├── components/      # Переиспользуемые компоненты
│   │   ├── pages/           # Страницы (Login, Query, Upload)
│   │   ├── services/        # Функции для вызова API
│   │   ├── types/           # TypeScript типы
│   │   └── context/         # UserContext
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml       # Оркестрация всех сервисов
├── Dockerfile.nginx         # Сборка Nginx с конфигом прокси
├── nginx-proxy.conf         # Конфигурация Nginx для прокси
├── .env.example             # (рекомендуется добавить) пример переменных
└── README.md

---

## 🔧 Конфигурация

Все основные параметры вынесены в классы `Settings` (`backend/core/config.py`):

- `Vector_Store_Settings` — модель эмбеддингов, параметры ретривера, путь к Chroma.
- `Text_Splitter_Settings` — размер чанков, перекрытие, разделители.
- `LLM_Settings` — API‑ключ, модель, base_url, температура.
- `PostgresSettings` — параметры подключения к БД.
- `Settings.DOCUMENTS_DIRECTORY`, `UPLOAD_TEMP_DIR` — пути к папкам для документов и временных файлов.

При необходимости изменить поведение (например, использовать другую модель эмбеддингов) можно отредактировать эти классы или передать соответствующие переменные окружения.

---

## 📝 Планы по развитию

- Добавить аутентификацию (JWT или сессии).
- Реализовать удаление диалогов и документов.
- Улучшить обработку ошибок и индикацию загрузки на фронтенде.
- Поддержка других форматов (txt, docx).
- Возможность выбора модели LLM через интерфейс.

---

## 🤝 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE) (если применимо).

---

## 📬 Контакты

Если у вас есть вопросы или предложения, создавайте issue в репозитории или пишите на [email protected]