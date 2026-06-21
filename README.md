# FastAPI Messenger

Полнофункциональный мессенджер с обменом сообщениями в реальном времени. Бэкенд реализован на **FastAPI** в соответствии с принципами DDD, фронтенд навайбкожен на **Vue 3**.

---

## 🧰 Технологический стек

### Backend
- **Python 3.12**
- **FastAPI** + **Uvicorn** (ASGI-сервер)
- **WebSockets** — обмен сообщениями в реальном времени
- **SQLAlchemy 2.0** (async) + **asyncpg** — работа с PostgreSQL
- **Redis** + **Redis Pub/Sub** — кэширование чатов, сообщений и токенов; отправка сообщений между инстансами
- **PyJWT** + **bcrypt** — аутентификация и хеширование паролей
- **Pydantic v2** / **pydantic-settings** — валидация и конфигурация
- **Pytest** - юнит и интеграционные тесты

### Frontend
- **Vue 3** (Composition API)
- **Vue Router 4**
- **Vite** — сборщик и dev-сервер

### Инфраструктура
- **Docker** + **Docker Compose**
- **PostgreSQL 16** (Alpine)
- **Redis 7** (Alpine)
- **Apache Kafka** - применяется для отправки логов

---

## 🏛 Архитектура

Проект построен по принципам **Domain-Driven Design**. Бизнес-логика изолирована от инфраструктуры и фреймворка, что упрощает тестирование и расширение.

```
app/
├── domain/             # Доменный слой: сущности, value objects, доменные исключения
│   ├── base/           # Базовые классы (Entity, ValueObject, BaseError)
│   ├── user/           # Домен пользователя
│   ├── chat/           # Домен чата
│   └── message/        # Домен сообщения
│
├── application/        # Слой приложения: use cases и сервисы
│   └── services/       # auth, chat, jwt, message, user сервисы
│
├── infrastructure/     # Инфраструктурный слой: реализация интерфейсов
│   ├── adapters/
│   │   └── repositories/   # Репозитории для PostgreSQL
│   ├── cache/              # Redis-кэши (chat, messages, token)
│   ├── database/
│   │   ├── postgresql/     # Подключение, mappers (ORM <-> domain)
│   │   └── redis/          # Подключение к Redis
│   └── websockets/         # ConnectionManager для WS-сессий
│
├── presentation/       # Презентационный слой: HTTP/WS API
│   └── api/
│       └── v1/
│           ├── dependencies/   # FastAPI DI (auth, services, repos, session)
│           ├── endpoints/
│           │   ├── http/       # auth_router, chat_router, messages_router
│           │   └── websockets/ # messages_ws
│           └── schemas/        # Pydantic-схемы запросов/ответов
│
└── core/               # Глобальные настройки (settings.py)
```

---

## ✨ Возможности

- 🔐 Регистрация и вход (JWT access + refresh-токены)
- 🔄 Автоматическое обновление access-токена через HttpOnly cookie
- 👥 Добавление пользователей в личные (direct) чаты
- 💬 Обмен сообщениями в реальном времени по WebSocket
- 📜 Получение списка чатов пользователя с превью
- ⚡ Кэширование чатов, сообщений и токенов в Redis
- 🐳 Полная контейнеризация через Docker Compose

---

## 🚀 Быстрый старт (Docker)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/TupichokTheF/fastapi-messanger.git
cd fastapi-messanger
```

### 2. Создать файл `.env`

Скопируйте `.env-example` в `.env` и заполните значения:

```env
POSTGRES_SERVER=postgres
POSTGRES_PORT=5432
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=messenger

REDIS_HOST=redis
REDIS_PORT=6379

JWT_SECRET_KEY=your_secret_key_here
```

### 3. Запустить контейнеры

```bash
docker compose up -d --build
```

После запуска поднимаются три сервиса:

| Сервис   | Контейнер       | Порт (host → container) |
|----------|-----------------|-------------------------|
| app      | `chat_app`      | `1111 → 8000`           |
| postgres | `chat_postgres` | `5433 → 5432`           |
| redis    | `chat_redis`    | `6378 → 6379`           |

API будет доступен на `http://localhost:1111`, документация Swagger — `http://localhost:1111/docs`.

### 4. Запустить фронтенд

```bash
cd frontend
npm install
npm run dev
```

Dev-сервер Vite поднимется на `http://localhost:5173` и проксирует запросы `/api` и WebSocket на бэкенд.

---

## 📡 API

Все маршруты находятся под префиксом `/api/v1`.

### Авторизация (`/auth`)

| Метод | Путь                | Описание                                  |
|-------|---------------------|-------------------------------------------|
| POST  | `/auth/sign_up`     | Регистрация нового пользователя           |
| POST  | `/auth/sign_in`     | Вход, выдача access + refresh-токенов     |
| POST  | `/auth/refresh`     | Обновление access-токена по cookie        |

### Чаты (`/chat`)

| Метод | Путь                  | Описание                                       |
|-------|-----------------------|------------------------------------------------|
| POST  | `/chat/add_direct_chat` | Создать личный чат с другим пользователем    |
| GET   | `/chat/get_chats`     | Получить список чатов текущего пользователя    |

### WebSocket (`/ws`)

| Путь                | Описание                                       |
|---------------------|------------------------------------------------|
| `/ws/send_message`  | Двусторонний канал для обмена сообщениями      |

Полная интерактивная документация доступна по адресу `/docs` (Swagger UI) или `/redoc`.

---

## 👤 PlayBoy

[**TupichokTheF**](https://github.com/TupichokTheF)
