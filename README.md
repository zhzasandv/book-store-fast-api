# Book Shop API

REST API для магазина книг на FastAPI + SQLAlchemy + SQLite.

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic v2
- Uvicorn
- SQLite

## Установка и запуск

### 1. Установить pyenv

```bash
curl https://pyenv.run | bash
```

Добавить в `~/.bashrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
```

```bash
source ~/.bashrc
```

### 2. Установить Python 3.12

```bash
pyenv install 3.12.0
```

### 3. Клонировать репозиторий и перейти в папку

```bash
cd book-backend
pyenv local 3.12.0
```

### 4. Создать и активировать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate
```

### 5. Установить зависимости

```bash
pip install -r requirements.txt
```

### 6. Настроить переменные окружения

```bash
cp .env.example .env
```

Задать `BASE_URL` в `.env`:

```env
BASE_URL=http://localhost:8000
```

### 7. Запустить сервер

```bash
uvicorn main:app --reload
```

Сервер запустится на `http://localhost:8000`. Таблицы в БД создаются автоматически при старте.

## Документация API

После запуска доступна по адресу: `http://localhost:8000/docs`

---

## Архитектура

```
Router → Service → Repository → Model
```

| Слой | Папка | Документация |
|------|-------|--------------|
| Router | `routers/` | [routers/README.md](routers/README.md) |
| Service | `services/` | [services/README.md](services/README.md) |
| Repository | `repositories/` | [repositories/README.md](repositories/README.md) |
| Model | `models/` | [models/README.md](models/README.md) |
| Schema | `schemas/` | [schemas/README.md](schemas/README.md) |
