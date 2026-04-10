# models/

ORM-модели SQLAlchemy. Все три сущности описаны в одном файле `book.py`.

---

## book.py

### `Author` → таблица `market_author`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Первичный ключ |
| `first_name` | String(30) | Имя |
| `last_name` | String(30) | Фамилия |

### `Genre` → таблица `market_genre`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Первичный ключ |
| `name` | String(20) | Название жанра |

### `Book` → таблица `market_book`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Первичный ключ |
| `name` | String(100) | Название книги |
| `price` | Numeric(7,2) | Цена |
| `title` | String(1000) | Описание |
| `publication_date` | String(15) | Дата публикации |
| `oblojka` | String | Имя файла обложки (опционально) |
| `genre_id` | ForeignKey | Ссылка на `market_genre.id` |

### Связи

- `Book` ↔ `Author` — Many-to-Many через промежуточную таблицу `market_book_authors`
- `Book` → `Genre` — Many-to-One (у книги один жанр, у жанра много книг)
