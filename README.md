# Mini App Corgi

Небольшое веб-приложение о корги. Главная страница приветствует пользователя, а на странице `/info` выводится информация о двух разновидностях корги и их фотографии.

## Что используется

- Python 3.11
- FastAPI и Uvicorn
- Jinja2 для HTML-шаблонов
- PostgreSQL 14
- SQLAlchemy
- Nginx
- Docker Compose

## Структура проекта

```text
.
├── app/
│   ├── main.py              # FastAPI-приложение и модель Photo
│   ├── requirements.txt     # Python-зависимости
│   ├── Dockerfile
│   ├── templates/            # HTML-шаблоны
│   └── static/               # CSS и изображения
├── nginx/default.conf        # Конфигурация прокси и статики
├── tests/test_main.py        # Базовые тесты главной страницы
└── docker-compose.yml        # Сервисы web, db и nginx
```

## Запуск через Docker Compose

Нужны установленные Docker и Docker Compose.

```bash
docker compose up --build
```

После запуска приложение доступно по адресу:

<http://localhost/>

Остановка контейнеров:

```bash
docker compose down
```

Данные PostgreSQL сохраняются в Docker volume `postgres_data`. Чтобы удалить контейнеры вместе с данными базы, используйте `docker compose down -v`.

## Страницы

- `/` — приветственная страница.
- `/info` — описание корги и галерея фотографий из базы данных.
- `/static/...` — CSS и изображения.

При первом запуске приложение создаёт таблицу `photos` и добавляет две записи:

- `corgi1.jpg` — валлийский пемброк;
- `corgi2.jpg` — валлийский кардиган.

## Переменные окружения

По умолчанию используется подключение:

```text
postgresql://postgres:postgres@db:5432/corgi_db
```

Можно указать другое подключение к базе через `DATABASE_URL`. Для отключения инициализации базы при запуске приложения используется `ENV=test`.

## Запуск без Docker

Из каталога `app` установите зависимости и запустите сервер:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

В этом режиме PostgreSQL должен быть доступен по адресу из `DATABASE_URL`.

## Тесты

Тесты проверяют доступность главной страницы и HTML-ответ:

```bash
ENV=test pytest
```

Переменная `ENV=test` нужна, чтобы тесты не пытались подключиться к PostgreSQL во время импорта приложения.
