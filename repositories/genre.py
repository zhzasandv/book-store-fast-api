from sqlalchemy.orm import Session
from models.book import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Genre]:
        return self.db.query(Genre).all()

    def get_by_id(self, genre_id: int) -> Genre | None:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def create(self, name: str) -> Genre:
        genre = Genre(name=name)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def update(self, genre: Genre, name: str | None) -> Genre:
        if name is not None:
            genre.name = name
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def delete(self, genre: Genre) -> None:
        self.db.delete(genre)
        self.db.commit()