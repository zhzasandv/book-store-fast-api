# repositories/

Слой работы с базой данных. Принимают SQLAlchemy-сессию, выполняют запросы, возвращают ORM-объекты.

---

## BookRepository (`book.py`)

| Метод | Описание |
|-------|----------|
| `get_all()` | Все книги с жадной загрузкой авторов и жанра (`joinedload`) |
| `get_by_id(book_id)` | Одна книга по id с авторами и жанром |
| `create(data, authors)` | Создаёт книгу, привязывает список авторов |
| `update(book, data, authors)` | Обновляет поля книги и/или список авторов |
| `delete(book)` | Удаляет книгу из БД |

`joinedload` используется для предотвращения проблемы N+1 — авторы и жанр загружаются одним запросом вместе с книгой.

---

## AuthorRepository (`author.py`)

| Метод | Описание |
|-------|----------|
| `get_all()` | Все авторы |
| `get_by_id(author_id)` | Один автор по id |
| `create(first_name, last_name)` | Создаёт автора |
| `update(author, first_name, last_name)` | Обновляет поля, пропускает `None`-значения |
| `delete(author)` | Удаляет автора из БД |

---

## GenreRepository (`genre.py`)

| Метод | Описание |
|-------|----------|
| `get_all()` | Все жанры |
| `get_by_id(genre_id)` | Один жанр по id |
| `create(name)` | Создаёт жанр |
| `update(genre, name)` | Обновляет название, пропускает `None` |
| `delete(genre)` | Удаляет жанр из БД |
