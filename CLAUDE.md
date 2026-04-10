# CLAUDE.md

Этот файл содержит инструкции для Claude Code (claude.ai/code) при работе с данным репозиторием.

## Команды

```bash
# Установка
python -
m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn main:app --reload

# Документация API доступна по адресу http://localhost:8000/docs
```

Скопируй `.env.example` в `.env` и задай `BASE_URL` перед запуском.

## Архитектура

Это **Book Shop API** на FastAPI + SQLAlchemy (SQLite) с 4-слойной архитектурой:

```
Router → Service → Repository → Model
```

- **`routers/`** — HTTP-слой, определяет эндпоинты, инжектирует сессию `db` и сервис
- **`services/`** — Бизнес-логика, бросает `HTTPException` при ошибках
- **`repositories/`** — SQLAlchemy-запросы с жадной загрузкой связей (`joinedload`)
- **`models/book.py`** — Все ORM-модели: `Author`, `Genre`, `Book` (один файл)
- **`schemas/`** — Pydantic v2 DTO: `*DTO` (ответ), `*CreateDTO`, `*UpdateDTO`

## Ключевые детали

- Все маршруты имеют префикс `/api/v1/` и регистрируются в `main.py`
- База данных: SQLite-файл `db_final.sqlite3`, сессия инжектируется через зависимость `get_db()`
- `Book` ↔ `Author` — связь Many-to-Many через таблицу `market_book_authors`; `Book` → `Genre` — Many-to-One
- `BookDTO` содержит вычисляемое поле `image_url`, собранное из переменной окружения `BASE_URL` + имя файла `oblojka`
- Статические файлы раздаются по пути `/media/` из директории `media/`
- CORS открыт (разрешены все источники)
