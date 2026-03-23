from sqlalchemy.orm import Session
from models.book import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Genre]:
        return self.db.query(Genre).all()
