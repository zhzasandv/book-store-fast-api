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