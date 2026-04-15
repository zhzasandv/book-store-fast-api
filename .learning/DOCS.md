# Book Shop — Полная документация проекта

## Содержание

1. [Обзор проекта](#1-обзор-проекта)
2. [Технологии](#2-технологии)
3. [Структура файлов](#3-структура-файлов)
4. [Архитектура](#4-архитектура)
5. [База данных](#5-база-данных)
6. [Бэкенд — слой за слоем](#6-бэкенд--слой-за-слоем)
   - [Точка входа — main.py](#61-точка-входа--mainpy)
   - [База данных — database.py](#62-база-данных--databasepy)
   - [Модели — models/book.py](#63-модели--modelsbookpy)
   - [Схемы (DTO) — schemas/](#64-схемы-dto--schemas)
   - [Репозитории — repositories/](#65-репозитории--repositories)
   - [Сервисы — services/](#66-сервисы--services)
   - [Роутеры — routers/](#67-роутеры--routers)
7. [API — полный справочник эндпоинтов](#7-api--полный-справочник-эндпоинтов)
8. [Фронтенд — Nuxt 3](#8-фронтенд--nuxt-3)
9. [Как работает поиск](#9-как-работает-поиск)
10. [Как работает image_url](#10-как-работает-image_url)
11. [Жизненный цикл запроса](#11-жизненный-цикл-запроса)
12. [Запуск проекта](#12-запуск-проекта)
13. [Правило обновления документации](#13-правило-обновления-документации)

---

## 1. Обзор проекта

**Book Shop** — это REST API для книжного магазина с каталогом книг. Включает:

- **Бэкенд** — FastAPI + SQLAlchemy + SQLite. Управляет книгами, авторами и жанрами.
- **Фронтенд** — Nuxt 3 (Vue 3 + TypeScript). Отображает каталог книг с поиском.

Приложение позволяет:
- просматривать список книг с обложками, авторами, жанрами и ценами
- искать книги по названию, автору или жанру (поиск на бэкенде)
- создавать, обновлять и удалять книги, авторов, жанры через API

**Документация должна обновляться вместе с кодом.** Если меняется поведение,
архитектура, API-контракт или добавляется новая возможность, этот файл нужно
переписать в соответствующем разделе или дополнить новым описанием.

---

## 2. Технологии

|       Слой       |   Технология   |               Для чего                    |
|------------------|----------------|-------------------------------------------|
| HTTP-сервер      | FastAPI        | Обработка запросов, авто-документация     |
| ORM              | SQLAlchemy     | Работа с БД через Python-объекты          |
| БД               | SQLite         | Хранение данных (файл `db_final.sqlite3`) |
| Валидация        | Pydantic v2    | Проверка входных данных, сериализация     |
| Фронтенд         | Nuxt 3 + Vue 3 | SPA-интерфейс каталога                    |
| Типизация        | TypeScript     | Типы для Book, Author, Genre на фронтенде |
| Переменные среды | python-dotenv  | Чтение `.env` файла                       |

---

## 3. Структура файлов

```
fast-api-back/
│
├── main.py                  # Точка входа: создаёт FastAPI app, подключает роутеры
├── database.py              # Конфигурация SQLAlchemy, функция get_db()
├── requirements.txt         # Зависимости Python
├── .env                     # Переменные среды (BASE_URL)
├── .env.example             # Пример .env файла
├── seed.py                  # Скрипт для заполнения БД тестовыми данными
├── db_final.sqlite3         # Файл базы данных SQLite
│
├── models/
│   └── book.py              # ORM-модели: Author, Genre, Book + таблица связи
│
├── schemas/
│   ├── book.py              # BookDTO, BookCreateDTO, BookUpdateDTO
│   ├── author.py            # AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO
│   └── genre.py             # GenreDTO, GenreCreateDTO, GenreUpdateDTO
│
├── repositories/
│   ├── book.py              # BookRepository — SQL-запросы для книг
│   ├── author.py            # AuthorRepository — SQL-запросы для авторов
│   └── genre.py             # GenreRepository — SQL-запросы для жанров
│
├── services/
│   ├── book.py              # BookService — бизнес-логика для книг
│   ├── author.py            # AuthorService — бизнес-логика для авторов
│   └── genre.py             # GenreService — бизнес-логика для жанров
│
├── routers/
│   ├── books.py             # Эндпоинты /api/v1/books
│   ├── authors.py           # Эндпоинты /api/v1/authors
│   └── genres.py            # Эндпоинты /api/v1/genres
│
├── media/
│   └── books/               # Изображения обложек книг (jpg, png)
│
└── frontend/                # Nuxt 3 приложение
    ├── nuxt.config.ts       # Конфигурация Nuxt
    ├── app.vue              # Корневой компонент
    ├── pages/
    │   └── index.vue        # Главная страница каталога
    ├── composables/
    │   └── useBooks.ts      # Логика загрузки и поиска книг
    └── types/
        └── book.ts          # TypeScript-типы: Book, Author, Genre
```

---

## 4. Архитектура

Бэкенд построен по **4-слойной архитектуре**. Каждый слой отвечает строго за своё:

```
HTTP-запрос от клиента
        │
        ▼
┌──────────────────┐
│     Router       │  ← Принимает HTTP, инжектирует зависимости, возвращает ответ
└────────┬─────────┘
         │ вызывает
         ▼
┌──────────────────┐
│     Service      │  ← Бизнес-логика: валидация, обработка ошибок, преобразование
└────────┬─────────┘
         │ вызывает
         ▼
┌──────────────────┐
│   Repository     │  ← Работа с БД: SQL-запросы через SQLAlchemy
└────────┬─────────┘
         │ использует
         ▼
┌──────────────────┐
│     Model        │  ← ORM-классы: описание таблиц и связей
└────────┬─────────┘
         │
         ▼
    SQLite БД
```

### Почему такая архитектура?

- **Router** не знает про SQL — только HTTP.
- **Service** не знает про HTTP — только логика.
- **Repository** не знает про бизнес-правила — только запросы.
- Если нужно заменить SQLite на PostgreSQL — меняешь только репозиторий.
- Если меняется бизнес-правило — меняешь только сервис.

---

## 5. База данных

### Схема таблиц

```
┌─────────────────────┐        ┌──────────────────────────┐
│    market_author    │        │       market_book        │
├─────────────────────┤        ├──────────────────────────┤
│ id          INTEGER │        │ id              INTEGER  │
│ first_name  VARCHAR │        │ name            VARCHAR  │
│ last_name   VARCHAR │        │ price           NUMERIC  │
└─────────────────────┘        │ title           VARCHAR  │
           │                   │ publication_date VARCHAR │
           │                   │ oblojka         VARCHAR  │  ← имя файла обложки
           │                   │ genre_id        INTEGER ─┼──┐
           │                   └──────────────────────────┘  │
           │                                                 │
           │  ┌──────────────────────────┐                   │
           │  │  market_book_authors     │                   │
           │  ├──────────────────────────┤                   │
           └──┤ author_id      INTEGER   │                   │
              │ book_id        INTEGER ──┼── (связь M:M)     │
              └──────────────────────────┘                   │
                                                             │
                                          ┌──────────────────┴───┐
                                          │    market_genre      │
                                          ├──────────────────────┤
                                          │ id      INTEGER      │
                                          │ name    VARCHAR      │
                                          └──────────────────────┘
```

### Связи

|      Связь    |      Тип     |   Таблица-посредник   |
|---------------|--------------|-----------------------|
| Book ↔ Author | Many-to-Many | `market_book_authors` |
| Book → Genre  | Many-to-One  | — (FK `genre_id`)     |

**Пример:** Одна книга может иметь двух авторов. Один автор может написать несколько книг. Жанр у книги всегда один.

---

## 6. Бэкенд — слой за слоем

### 6.1 Точка входа — `main.py`

```python
app = FastAPI(title="Books API", version="v1")
```

Делает три вещи:
1. **Создаёт таблицы** — `Base.metadata.create_all(bind=engine)` при запуске
2. **Настраивает CORS** — разрешает запросы с любого источника (фронтенд localhost:3000)
3. **Монтирует** статические файлы (`/media/`) и регистрирует три роутера

```python
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
```

---

### 6.2 База данных — `database.py`

Создаёт движок SQLAlchemy и фабрику сессий:

```python
DATABASE_URL = "sqlite:///./db_final.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

`check_same_thread=False` нужен потому, что FastAPI использует несколько потоков, а SQLite по умолчанию не разрешает доступ из разных потоков.

Функция `get_db()` — **dependency injection** для FastAPI:

```python
def get_db():
    db = SessionLocal()  # открываем сессию
    try:
        yield db          # отдаём её роутеру
    finally:
        db.close()        # закрываем после запроса
```

---

### 6.3 Модели — `models/book.py`

Три ORM-класса + таблица-посредник:

**Таблица Many-to-Many (не класс, просто объект Table):**
```python
book_author = Table(
    "market_book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("market_book.id")),
    Column("author_id", Integer, ForeignKey("market_author.id")),
)
```

**Author:**
```python
class Author(Base):
    __tablename__ = "market_author"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    books = relationship("Book", secondary=book_author, back_populates="authors")
```

**Genre:**
```python
class Genre(Base):
    __tablename__ = "market_genre"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    books = relationship("Book", back_populates="genre")
```

**Book:**
```python
class Book(Base):
    __tablename__ = "market_book"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(7, 2))      # до 99999.99
    title = Column(String(1000))        # описание книги
    publication_date = Column(String(15))
    oblojka = Column(String, nullable=True)  # имя файла: "cover.jpg"
    genre_id = Column(Integer, ForeignKey("market_genre.id"))
    genre = relationship("Genre", back_populates="books")
    authors = relationship("Author", secondary=book_author, back_populates="books")
```

---

### 6.4 Схемы (DTO) — `schemas/`

DTO (Data Transfer Object) — это Pydantic-модели для передачи данных между слоями и клиентом. Есть три вида:

| Суффикс | Назначение | Пример |
|---|---|---|
| `DTO` | Ответ клиенту (чтение) | `BookDTO` |
| `CreateDTO` | Тело POST-запроса (создание) | `BookCreateDTO` |
| `UpdateDTO` | Тело PUT-запроса (обновление, все поля опциональны) | `BookUpdateDTO` |

**BookDTO** — содержит вычисляемое поле `image_url`:

```python
class BookDTO(BaseModel):
    id: int
    name: str
    price: float
    title: str
    publication_date: str
    genre: GenreDTO       # вложенный объект жанра
    authors: list[AuthorDTO]  # список авторов
    oblojka: Optional[str] = None

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.oblojka:
            return f"{BASE_URL}/media/{self.oblojka}"
        return None

    model_config = {"from_attributes": True}  # позволяет создавать из ORM-объектов
```

`from_attributes = True` означает, что Pydantic умеет читать поля из SQLAlchemy-объектов напрямую (без `.dict()`).

**BookCreateDTO** — для создания книги:
```python
class BookCreateDTO(BaseModel):
    name: str
    price: float
    title: str
    publication_date: str
    genre_id: int
    author_ids: list[int]   # список ID авторов
    oblojka: Optional[str] = None
```

**BookUpdateDTO** — все поля опциональны (`None` = не менять):
```python
class BookUpdateDTO(BaseModel):
    name: str | None = None
    price: float | None = None
    # ... и т.д.
```

---

### 6.5 Репозитории — `repositories/`

Репозиторий — единственное место, где пишутся SQL-запросы.

**BookRepository** — самый сложный, использует `joinedload` для жадной загрузки:

```python
def _with_relations(self):
    return self.db.query(Book).options(
        joinedload(Book.authors),
        joinedload(Book.genre)
    )
```

`joinedload` — это команда SQLAlchemy: "загружай авторов и жанр сразу вместе с книгой в одном JOIN-запросе, не делай отдельные запросы". Без этого при обращении к `book.authors` SQLAlchemy делал бы дополнительный запрос на каждую книгу (проблема N+1).

Репозиторий также содержит небольшие вспомогательные методы для бизнес-логики
книг:

```python
def get_authors_by_ids(self, author_ids: list[int]) -> list[Author]:
    return self.db.query(Author).filter(Author.id.in_(author_ids)).all()

def genre_exists(self, genre_id: int) -> bool:
    return self.db.query(Genre.id).filter(Genre.id == genre_id).first() is not None
```

Эти методы оставляют SQL-запросы в слое `Repository`, а `Service` использует их
для проверки входных данных.

**Метод поиска `search(q)`:**

```python
def search(self, q: str) -> list[Book]:
    pattern = f"%{q}%"
    return (
        self._with_relations()
        .join(Book.genre)
        .join(Book.authors)
        .filter(
            Book.name.ilike(pattern) |
            Book.title.ilike(pattern) |
            Author.first_name.ilike(pattern) |
            Author.last_name.ilike(pattern) |
            (Author.first_name + " " + Author.last_name).ilike(pattern) |
            Genre.name.ilike(pattern)
        )
        .distinct()
        .all()
    )
```

- `ilike` — регистронезависимый LIKE (работает и с "python", и с "Python")
- `%q%` — ищет подстроку в любом месте строки
- `distinct()` — убирает дубли (книга с двумя авторами иначе появится дважды)
- Ищет одновременно по: названию книги, описанию, имени, фамилии автора, полному имени автора, жанру

---

### 6.6 Сервисы — `services/`

Сервис содержит бизнес-логику и бросает `HTTPException` при ошибках.

**BookService** — пример метода `create`:

```python
def create(self, data: BookCreateDTO) -> BookDTO:
    self._ensure_genre_exists(data.genre_id)
    authors = self._get_authors(data.author_ids)
    book_data = data.model_dump(exclude={"author_ids"})  # убираем author_ids из словаря
    book = self.repository.create(book_data, authors)
    return BookDTO.model_validate(book)  # конвертируем ORM → DTO
```

Метод `_get_authors` проверяет, что все переданные `author_ids` существуют в БД.
Повторяющиеся ID считаются одним автором, чтобы проверка не ломалась на дублях:

```python
def _get_authors(self, author_ids: list[int]) -> list[Author]:
    unique_author_ids = set(author_ids)
    authors = self.repository.get_authors_by_ids(author_ids)
    if len(authors) != len(unique_author_ids):
        raise HTTPException(status_code=404, detail="One or more authors not found")
    return authors
```

Если хотя бы один ID не найден — клиент получит `404 Not Found`.

Метод `_ensure_genre_exists` проверяет жанр перед созданием или обновлением
книги:

```python
def _ensure_genre_exists(self, genre_id: int) -> None:
    if not self.repository.genre_exists(genre_id):
        raise HTTPException(status_code=404, detail="Genre not found")
```

Это не даёт создать или обновить книгу с несуществующим `genre_id`.

---

### 6.7 Роутеры — `routers/`

Роутер определяет HTTP-эндпоинты и связывает их с сервисом через **dependency injection**.

**Dependency injection в FastAPI:**

```python
def get_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(BookRepository(db))
```

FastAPI автоматически:
1. Вызывает `get_db()` → получает сессию БД
2. Создаёт `BookRepository(db)` с этой сессией
3. Создаёт `BookService(repository)` с этим репозиторием
4. Передаёт сервис в функцию-обработчик

```python
@router.post("/", response_model=BookDTO, status_code=201)
def create_book(data: BookCreateDTO, service: BookService = Depends(get_service)):
    return service.create(data)
```

Роутер не достаёт `db` из `service.repository`. Он только принимает HTTP-запрос,
вызывает метод сервиса и возвращает результат. Это сохраняет разделение слоёв:
`Router → Service → Repository → Model`.

---

## 7. API — полный справочник эндпоинтов

Интерактивная документация доступна по адресу `http://localhost:8000/docs`

### Книги `/api/v1/books`

| Метод | URL | Описание | Тело запроса | Ответ |
|---|---|---|---|---|
| GET | `/api/v1/books/` | Каталог книг с пагинацией и фильтрами `page`, `page_size`, `q`, `genre_id`, `author_id` | — | `BookListDTO` |
| GET | `/api/v1/books/search?q=текст` | Поиск книг | — | `list[BookDTO]` |
| GET | `/api/v1/books/{id}` | Книга по ID | — | `BookDTO` |
| POST | `/api/v1/books/` | Создать книгу | `BookCreateDTO` | `BookDTO` (201) |
| PUT | `/api/v1/books/{id}` | Обновить книгу | `BookUpdateDTO` | `BookDTO` |
| DELETE | `/api/v1/books/{id}` | Удалить книгу | — | 204 No Content |

**Пример BookCreateDTO:**
```json
{
  "name": "Clean Code",
  "price": 4500.00,
  "title": "Книга о написании чистого кода",
  "publication_date": "2008-01-01",
  "genre_id": 1,
  "author_ids": [1, 2],
  "oblojka": "clean_code.jpg"
}
```

**Пример BookDTO (ответ):**
```json
{
  "id": 1,
  "name": "Clean Code",
  "price": 4500.0,
  "title": "Книга о написании чистого кода",
  "publication_date": "2008-01-01",
  "genre": { "id": 1, "name": "Программирование" },
  "authors": [
    { "id": 1, "first_name": "Robert", "last_name": "Martin" }
  ],
  "oblojka": "clean_code.jpg",
  "image_url": "http://localhost:8000/media/clean_code.jpg"
}
```

### Авторы `/api/v1/authors`

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/v1/authors/` | Все авторы |
| GET | `/api/v1/authors/{id}` | Автор по ID |
| POST | `/api/v1/authors/` | Создать автора |
| PUT | `/api/v1/authors/{id}` | Обновить автора |
| DELETE | `/api/v1/authors/{id}` | Удалить автора |

### Жанры `/api/v1/genres`

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/v1/genres/` | Все жанры |
| GET | `/api/v1/genres/{id}` | Жанр по ID |
| POST | `/api/v1/genres/` | Создать жанр |
| PUT | `/api/v1/genres/{id}` | Обновить жанр |
| DELETE | `/api/v1/genres/{id}` | Удалить жанр |

### Статические файлы

```
GET /media/{filename}   → возвращает файл из папки media/
```

Пример: `GET /media/clean_code.jpg` → отдаёт изображение обложки.

---

## 8. Фронтенд — Nuxt 3

### Структура

```
frontend/
├── app.vue              # Общая оболочка: навигация, бренд, глобальный поиск
├── nuxt.config.ts       # Конфигурация: apiBase = http://localhost:8000
├── pages/
│   ├── index.vue        # Главная страница
│   ├── library.vue      # Каталог книг с фильтрами и пагинацией
│   ├── genres.vue       # Список жанров
│   └── authors.vue      # Список авторов
├── composables/
│   ├── useBooks.ts      # Загрузка каталога с query-параметрами
│   └── useLibraryQuery.ts # Сборка query для переходов в библиотеку
└── types/
    └── book.ts          # TypeScript-интерфейсы
```

### `app.vue` — общая оболочка

`app.vue` отвечает за общий фон, шапку и глобальный поиск.

На главной странице показываются:

- навигация: Главная, Библиотека, Жанры, Авторы
- компактный логотип и название сайта
- поисковая строка

В разделах `/library`, `/genres`, `/authors` шапка становится компактной:
логотип и название сайта скрываются, но навигация по разделам остаётся сверху
рядом с поиском. Поиск всегда ведёт в `/library` и передаёт текст через
query-параметр `q`. Если поисковик очистить и отправить пустым, параметр `q`
удаляется из URL, поэтому каталог возвращается к результатам без текстового
поиска.

Главная страница не занимает всю высоту экрана: hero-блок уменьшен, чтобы
контент начинался выше и страница выглядела собраннее. При переходе в разделы
логотип и название не удаляются резко, а плавно схлопываются и исчезают, пока
поисковик мягко поднимается в компактную шапку.

### `types/book.ts` — TypeScript интерфейсы

```typescript
export interface Author {
  id: number
  first_name: string
  last_name: string
}

export interface Genre {
  id: number
  name: string
}

export interface Book {
  id: number
  name: string
  price: number
  title: string
  publication_date: string
  genre: Genre
  authors: Author[]
  image_url: string | null
}
```

Эти типы зеркально повторяют Pydantic DTO с бэкенда.

### `composables/useBooks.ts` — логика загрузки каталога

```typescript
export function useBooks() {
  const config = useRuntimeConfig()
  const route = useRoute()
  // читает page, q, genre_id, author_id из route.query
  // запрашивает /api/v1/books/ с этими параметрами
}
```

- `useFetch` — встроенный composable Nuxt для HTTP-запросов
- каталог использует `/api/v1/books/`
- фильтры и поиск живут в URL query, поэтому ссылкой можно поделиться
- при смене `q`, `genre_id`, `author_id` или `page` список книг перезагружается
- `useLibraryQuery` использует `null` как явную команду удалить query-параметр;
  это нужно для сброса поиска, жанра, автора и страницы
- вместе с `genre_id` и `author_id` в URL сохраняются `genre_name` и
  `author_name`, чтобы выбранное название фильтра оставалось видимым после
  перезагрузки страницы

### `pages/index.vue` — главная страница

Главная страница содержит компактную информационную карточку и быстрые переходы
в библиотеку, жанры и авторов. Основной поиск расположен в общей шапке из
`app.vue`, поэтому на главной нет отдельного второго поискового поля.

### `pages/library.vue` — библиотека

Страница библиотеки показывает каталог книг, фильтры по жанру и автору,
состояния загрузки/ошибки/пустого результата и пагинацию. Заголовок раздела
остаётся внутри страницы, а глобальная шапка сверху в этом разделе показывает
навигацию по разделам и поисковик без логотипа сайта.

Фильтры библиотеки синхронизированы с URL. Если пользователь пришёл из карточки
жанра или автора, `genre_id` или `author_id` из query сразу выставляет выбранное
значение в соответствующем `<select>`. Если страница обновлена и список жанров
или авторов ещё загружается, название выбранного фильтра берётся из
`genre_name` или `author_name` в URL, поэтому в месте "Все жанры" или
"Все авторы" остаётся выбранное название.

### `pages/genres.vue` и `pages/authors.vue`

Страницы показывают карточки жанров и авторов. Клик по карточке переводит в
`/library` с активным фильтром `genre_id` или `author_id`.

---

## 9. Как работает поиск

```
Пользователь вводит текст
        │
        ▼
useBooks.ts (фронтенд)
  searchQuery меняется → useFetch делает новый запрос
        │
        ▼
GET /api/v1/books/search?q=python
        │
        ▼
books.py router → BookService.search(q)
        │
        ▼
BookRepository.search(q):
  SELECT DISTINCT book.* 
  FROM market_book
  JOIN market_genre ON ...
  JOIN market_book_authors ON ...
  JOIN market_author ON ...
  WHERE book.name ILIKE '%python%'
     OR book.title ILIKE '%python%'
     OR author.first_name ILIKE '%python%'
     OR author.last_name ILIKE '%python%'
     OR (author.first_name || ' ' || author.last_name) ILIKE '%python%'
     OR genre.name ILIKE '%python%'
        │
        ▼
Список Book ORM-объектов → список BookDTO → JSON
        │
        ▼
Фронтенд обновляет сетку карточек
```

---

## 10. Как работает `image_url`

Поле `oblojka` в БД хранит только **имя файла**, например `"clean_code.jpg"`.

При сериализации в `BookDTO` вычисляемое поле `image_url` собирает полный URL:

```python
@computed_field
@property
def image_url(self) -> Optional[str]:
    if self.oblojka:
        return f"{BASE_URL}/media/{self.oblojka}"
    return None
```

`BASE_URL` берётся из `.env`:
```
BASE_URL=http://localhost:8000
```

Итоговый URL: `http://localhost:8000/media/clean_code.jpg`

FastAPI раздаёт этот файл через `StaticFiles`:
```python
app.mount("/media", StaticFiles(directory="media"), name="media")
```

То есть файл должен физически лежать в папке `media/clean_code.jpg`.

---

## 11. Жизненный цикл запроса

Разберём на примере: `GET /api/v1/books/42`

```
1. FastAPI принимает запрос GET /api/v1/books/42

2. Вызывается get_service():
   - get_db() создаёт сессию SQLAlchemy
   - BookRepository(db) — репозиторий с этой сессией
   - BookService(repository) — сервис с этим репозиторием

3. Вызывается get_book(book_id=42, service=...)

4. service.get_by_id(42):
   - repository.get_by_id(42)
   - SQL: SELECT * FROM market_book
           LEFT JOIN market_book_authors ...
           LEFT JOIN market_author ...
           LEFT JOIN market_genre ...
           WHERE market_book.id = 42
   - Если None → raise HTTPException(404)

5. BookDTO.model_validate(book):
   - Pydantic читает поля ORM-объекта
   - Вычисляет image_url из oblojka
   - Возвращает DTO

6. FastAPI сериализует BookDTO в JSON

7. get_db() finally → db.close()

8. Клиент получает JSON-ответ
```

---

## 12. Запуск проекта

### Бэкенд

```bash
# 1. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate       # Linux/Mac
# или: venv\Scripts\activate   # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить переменные среды
cp .env.example .env
# Отредактировать .env: BASE_URL=http://localhost:8000

# 4. (опционально) Заполнить БД тестовыми данными
python seed.py

# 5. Запустить сервер
uvicorn main:app --reload
```

Сервер запустится на `http://localhost:8000`
Документация API: `http://localhost:8000/docs`

### Фронтенд

```bash
cd frontend

# Установить зависимости Node.js
npm install

# Запустить dev-сервер
npm run dev
```

Фронтенд запустится на `http://localhost:3000`

### Переменные среды

| Файл | Переменная | Значение по умолчанию | Описание |
|---|---|---|---|
| `.env` (бэкенд) | `BASE_URL` | `http://localhost:8000` | Базовый URL для формирования `image_url` |
| `frontend/.env` | — | — | (опционально) можно переопределить `apiBase` |
| `frontend/nuxt.config.ts` | `apiBase` | `http://localhost:8000` | URL бэкенда для фронтенда |

---

## 13. Правило обновления документации

При каждом изменении кода нужно проверять, затрагивает ли оно документацию.

Обновлять `.learning/DOCS.md` обязательно, если:

- изменились API-эндпоинты, параметры запроса, DTO или формат ответа
- изменилась логика сервисов, репозиториев или жизненный цикл запроса
- добавлены новые файлы, слои, зависимости или команды запуска
- исправлена ошибка, которая меняет поведение приложения

Если раздел уже существует, его нужно переписать актуально. Если подходящего
раздела нет, нужно добавить новый.
