# FastAPI Messenger

Мессенджер с обменом сообщениями в реальном времени. Бэкенд на **FastAPI**, спроектирован по принципам **DDD / чистой архитектуры**; фронтенд на **Vue 3** (сгенерирован с помощью AI и служит витриной для бэкенда).

---

## 🧰 Технологический стек

**Backend:** Python 3.12 · FastAPI + Uvicorn · WebSockets · SQLAlchemy 2.0 (async) + asyncpg · PostgreSQL 16 · Redis 7 (кэш + Pub/Sub) · Apache Kafka (доставка логов) · PyJWT + bcrypt · Pydantic v2

**Качество кода:** pytest (юнит-тесты доменного слоя) · ruff

**Инфраструктура:** Docker + Docker Compose

**Frontend:** Vue 3 (Composition API) · Vue Router 4 · Vite

---

## 🏛 Архитектура

Бизнес-логика изолирована от фреймворка и инфраструктуры: зависимости направлены внутрь, внешние технологии подключаются к ядру через порты (абстрактные интерфейсы) и адаптеры.

```
app/
├── domain/             # Ядро: сущности, value objects, доменные исключения,
│   ├── base/           # порты репозиториев. Зависит только от stdlib.
│   ├── user/
│   ├── chat/
│   └── message/
│
├── application/        # Сценарии использования: сервисы, DTO.
│   └── services/       # Зависит только от domain.
│
├── infrastructure/     # Driven-адаптеры: реализации портов.
│   ├── adapters/repositories/  # PostgreSQL-репозитории
│   ├── cache/                  # Redis-кэши (chat, messages, token)
│   ├── database/               # Подключения; императивный маппинг ORM ↔ domain
│   ├── brockers/kafka/         # Продюсер логов
│   └── websockets/             # ConnectionManager WS-сессий
│
├── presentation/       # Driving-адаптеры: HTTP/WS API.
│   └── api/v1/
│       ├── dependencies/       # Composition root: сборка графа через DI FastAPI
│       ├── endpoints/          # Роутеры (http/, websockets/)
│       └── schemas/            # Pydantic-схемы запросов/ответов
│
└── core/               # Общие настройки (pydantic-settings)
```

---

## 🧠 Архитектурные решения

**Императивный маппинг SQLAlchemy вместо декларативного.** Доменные сущности — чистые dataclass'ы без наследования от `DeclarativeBase`; соответствие «сущность ↔ таблица» описано отдельно в `mappers.py` (включая `composite` для value objects). Домен не знает о существовании ORM и тестируется без базы. Цена — более сложная конфигурация маппинга и меньше «магии из коробки».

**Гонка при создании личного чата закрыта на уровне БД.** Проверка «чат уже существует» в коде не атомарна: два конкурентных запроса могли создать дубликат. Решение из двух обязательных половин: инвариант нормализации пары (`first_user < second_user`) живёт в доменной фабрике `DirectChat.create()`, а уникальность гарантирует `UniqueConstraint` в PostgreSQL. Нарушение constraint'а транслируется на границе слоя: репозиторий ловит `IntegrityError` и бросает доменное `ChatAlreadyExist` — слой приложения не знает про SQLAlchemy.

**Redis-схема под паттерны доступа мессенджера.** Списки чатов пользователя — sorted sets со score по времени активности (сортировка «недавние сверху» бесплатно), превью чатов — hashes, история — последние 50 сообщений на чат с обрезкой через `ZREMRANGEBYRANK`. Команды батчуются пайплайнами.

**Доставка сообщений между инстансами через Redis Pub/Sub.** WebSocket-соединения живут в памяти конкретного процесса, поэтому сообщение публикуется в канал чата, и каждый инстанс сам доставляет его своим подключённым клиентам — приложение готово к горизонтальному масштабированию.

**Неблокирующее логирование в Kafka.** Хендлер логгера — синхронный и может вызываться вне event loop, поэтому записи попадают в `asyncio.Queue` через `call_soon_threadsafe`, а фоновая задача отправляет их в Kafka. Медленный брокер не тормозит обработку запросов.

**Известный техдолг (осознанный):** кэш-классы внедряются в сервисы как конкретные реализации — это нарушение DIP, план миграции: порты `AbstractChatCache` / `AbstractMessagesCache` в слое application с методами-намерениями вместо протокола пайплайна. Также в планах Alembic вместо `metadata.create_all()` и read-through-фолбэк из PostgreSQL при промахе кэша.

---

## ✨ Возможности

- 🔐 Регистрация и вход: JWT access + refresh; refresh — в HttpOnly cookie и в Redis с TTL (отзывы сессий)
- 👥 Создание личных (direct) чатов
- 💬 Обмен сообщениями в реальном времени по WebSocket
- 📜 Список чатов с превью, отсортированный по активности
- 🕓 История последних сообщений чата
- ⚡ Кэширование чатов, сообщений и токенов в Redis
- 🐳 Контейнеризация через Docker Compose

---

## 🚀 Быстрый старт (Docker)

**1. Клонировать репозиторий**

```bash
git clone https://github.com/TupichokTheF/fastapi-messanger.git
cd fastapi-messanger
```

**2. Создать `.env`** — скопируйте `.env-example` и заполните:

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

**3. Запустить контейнеры**

```bash
docker compose up -d --build
```

| Сервис   | Контейнер       | Порт (host → container) |
|----------|-----------------|-------------------------|
| app      | `chat_app`      | `1111 → 8000`           |
| postgres | `chat_postgres` | `5433 → 5432`           |
| redis    | `chat_redis`    | `6378 → 6379`           |

API — `http://localhost:1111`, Swagger — `http://localhost:1111/docs`.

**4. Запустить фронтенд**

```bash
cd frontend
npm install
npm run dev
```

Vite поднимется на `http://localhost:5173` и проксирует `/api` и WebSocket на бэкенд.

---

## 🧪 Тесты и линтер

```bash
pytest tests/          # юнит-тесты доменной модели и кэша
ruff check app/        # статический анализ
```

---

## 📡 API

Все маршруты — под префиксом `/api/v1`. Полная интерактивная документация: `/docs` (Swagger UI) или `/redoc`.

### Авторизация (`/auth`)

| Метод | Путь            | Описание                              |
|-------|-----------------|----------------------------------------|
| POST  | `/auth/sign_up` | Регистрация нового пользователя        |
| POST  | `/auth/sign_in` | Вход, выдача access + refresh-токенов  |
| POST  | `/auth/refresh` | Обновление access-токена по cookie     |

### Чаты (`/chat`)

| Метод | Путь                    | Описание                                    |
|-------|-------------------------|---------------------------------------------|
| POST  | `/chat/add_direct_chat` | Создать личный чат с другим пользователем   |
| GET   | `/chat/get_chats`       | Список чатов текущего пользователя          |

### Сообщения (`/message`)

| Метод | Путь                  | Описание                              |
|-------|-----------------------|----------------------------------------|
| GET   | `/message/get_latest` | Последние сообщения чата               |

### WebSocket (`/ws`)

| Путь               | Описание                                  |
|--------------------|-------------------------------------------|
| `/ws/send_message` | Двусторонний канал для обмена сообщениями |

---

## 👤 Автор

[**TupichokTheF**](https://github.com/TupichokTheF)
