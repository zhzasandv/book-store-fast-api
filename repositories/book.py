from sqlalchemy.orm import Session, joinedload
from models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Book]:
        return self.db.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.genre)
        ).all()
