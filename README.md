# botofarm-service

### Установка зависимостей

```bash
poetry install
```

### Настройка

Скопируйте `.env`

```bash
cp .env.example .env
```

### Запуск в Docker

```bash
make up
```

Или вручную:
```bash
docker-compose up --build 
```

- Сервис будет доступен по ссылке: http://localhost:8000

Остановка:
```bash
make down
```
## Endpoints

### Авторизация

Все эндпоинты требуют авторизации через токен `admin-secret`.

- `POST /users/` - создание пользователя
- `GET /users/` - получение списка пользователей
- `POST /users/acquire-lock` - блокировка пользователя
- `POST /users/release-lock` - разблокировка пользователя

**Swagger UI**: http://localhost:8000/docs

## Тесты

Запуск тестов:
```bash
make test
```

## Структура проекта


- `app/entities/` - доменные сущности
- `app/use_cases/` - бизнес-логика
- `app/repositories/` - работа с данными
- `app/handlers/` - HTTP обработчики
- `app/infrastructure/` - инфраструктурный код
- `app/schemas/` - Pydantic схемы
