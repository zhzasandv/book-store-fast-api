from sqlalchemy.orm import Session
from models.book import Author


class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Author]:
        return self.db.query(Author).all()
