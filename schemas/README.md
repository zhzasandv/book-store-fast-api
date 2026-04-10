# schemas/

Pydantic v2 DTO для валидации входных данных и сериализации ответов.

Каждая сущность имеет три схемы:
- `*DTO` — ответ API (чтение)
- `*CreateDTO` — тело запроса при создании
- `*UpdateDTO` — тело запроса при обновлении (все поля опциональны)

---

## book.py

**`BookDTO`**

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Идентификатор |
| `name` | str | Название |
| `price` | float | Цена |
| `title` | str | Описание |
| `publication_date` | str | Дата публикации |
| `genre` | GenreDTO | Жанр (вложенный объект) |
| `authors` | list[AuthorDTO] | Авторы (вложенный список) |
| `oblojka` | str \| None | Имя файла обложки |
| `image_url` | str \| None | Вычисляемое поле: `BASE_URL/media/{oblojka}` |

**`BookCreateDTO`**

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | str | Название |
| `price` | float | Цена |
| `title` | str | Описание |
| `publication_date` | str | Дата публикации |
| `genre_id` | int | id жанра |
| `author_ids` | list[int] | Список id авторов |
| `oblojka` | str \| None | Имя файла обложки |

**`BookUpdateDTO`** — все поля аналогичны `BookCreateDTO`, но опциональны.

---

## author.py

**`AuthorDTO`**

| Поле | Тип |
|------|-----|
| `id` | int |
| `first_name` | str |
| `last_name` | str |

**`AuthorCreateDTO`** — `first_name`, `last_name`.

**`AuthorUpdateDTO`** — оба поля опциональны.

---

## genre.py

**`GenreDTO`**

| Поле | Тип |
|------|-----|
| `id` | int |
| `name` | str |

**`GenreCreateDTO`** — `name`.

**`GenreUpdateDTO`** — `name` опционально.
