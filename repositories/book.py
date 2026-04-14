from sqlalchemy.orm import Session, joinedload
from models.book import Book, Author, Genre


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def _with_relations(self):
        return self.db.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.genre)
        )

    def get_all(self) -> list[Book]:
        return self._with_relations().all()

    def _apply_filters(
        self,
        query,
        q: str | None = None,
        genre_id: int | None = None,
        author_id: int | None = None,
    ):
        needs_genre_join = bool(q)
        needs_author_join = bool(q) or author_id is not None

        if needs_genre_join:
            query = query.join(Book.genre)

        if needs_author_join:
            query = query.join(Book.authors)

        if q:
            pattern = f"%{q}%"
            query = (
                query
                .filter(
                    Book.name.ilike(pattern) |
                    Book.title.ilike(pattern) |
                    Author.first_name.ilike(pattern) |
                    Author.last_name.ilike(pattern) |
                    (Author.first_name + " " + Author.last_name).ilike(pattern) |
                    Genre.name.ilike(pattern)
                )
            )

        if genre_id is not None:
            query = query.filter(Book.genre_id == genre_id)

        if author_id is not None:
            query = query.filter(Author.id == author_id)

        return query

    def get_catalog(
        self,
        page: int,
        page_size: int,
        q: str | None = None,
        genre_id: int | None = None,
        author_id: int | None = None,
    ) -> tuple[list[Book], int]:
        filtered_ids = self._apply_filters(
            self.db.query(Book.id),
            q=q,
            genre_id=genre_id,
            author_id=author_id,
        ).distinct()

        total = filtered_ids.count()

        book_ids = [
            book_id
            for (book_id,) in (
                filtered_ids
                .order_by(Book.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
        ]

        if not book_ids:
            return [], total

        books = (
            self._with_relations()
            .filter(Book.id.in_(book_ids))
            .order_by(Book.id)
            .all()
        )

        books_by_id = {book.id: book for book in books}
        ordered_books = [books_by_id[book_id] for book_id in book_ids if book_id in books_by_id]
        return ordered_books, total

    def search(self, q: str) -> list[Book]:
        return (
            self._apply_filters(self._with_relations(), q=q)
            .distinct()
            .all()
        )

    def get_by_id(self, book_id: int) -> Book | None:
        return self._with_relations().filter(Book.id == book_id).first()

    def create(self, data: dict, authors: list[Author]) -> Book:
        book = Book(**data)
        book.authors = authors
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return self.get_by_id(book.id)

    def update(self, book: Book, data: dict, authors: list[Author] | None) -> Book:
        for key, value in data.items():
            setattr(book, key, value)
        if authors is not None:
            book.authors = authors
        self.db.commit()
        return self.get_by_id(book.id)

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
