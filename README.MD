Выполнил: Тер-Погосян Юрий М25-555

# Защищенный API для работы с большой языковой моделью

Серверное приложение на FastAPI, предоставляющее защищённый API для взаимодействия с большой языковой моделью (LLM) через сервис OpenRouter.

## Установочные операции

### Для запуска

Клонирование проекта

`git clone git@github.com:yura11yura/llm-p_Ter-Poghosyan_Yurii_M25-555.git`

`cd llm-p_Ter-Poghosyan_Yurii_M25-555`

Создание виртуального окружения

`uv venv`
`.venv\Scripts\activate.bat`

Установка зависимостей

`uv pip compile pyproject.toml -o requirements.txt`

`uv pip install -r requirements.txt`

Шаблон .env файла:

```
APP_NAME=llm-p
ENV=local

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./app.db

OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=llm-fastapi-openrouter
```

Запуск приложения

`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Приложение будет доступно по ссылке: http://127.0.0.1:8000/docs

## Эндпоинты проекта

| Метод | Эндпоинт | Описание | Доступ | Тело запроса | Ответ |
|-------|----------|----------|--------|--------------|-------|
| POST | `/auth/register` | Регистрация нового пользователя | Открытый | `{"email": "string", "password": "string"}` | `{"id": 0, "email": "string", "role": "string"}` |
| POST | `/auth/login` | Вход и получение JWT токена | Открытый | form-data: `username`, `password` | `{"access_token": "string", "token_type": "bearer"}` |
| GET | `/auth/me` | Профиль текущего пользователя | JWT | — | `{"id": 0, "email": "string", "role": "string"}` |
| POST | `/chat` | Отправка запроса к LLM | JWT | `{"prompt": "string", "system": "string", "max_history": 12, "temperature": 0.7}` | `{"answer": "string"}` |
| GET | `/chat/history` | История диалога | JWT | Query: `limit` (int, по умолчанию 50) | `{"history": [...]}` |
| DELETE | `/chat/history` | Очистка истории | JWT | — | 204 No Content |
| GET | `/health` | Проверка работоспособности | Открытый | — | `{"status": "ok", "environment": "string"}` |

## Демонстрация работы
![Alt text](/images/auth-login.png?raw=true "Optional Title")
