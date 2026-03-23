from sqlalchemy.orm import Session
from models.book import Author


class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Author]:
        return self.db.query(Author).all()

    def get_by_id(self, author_id: int) -> Author | None:
        return self.db.query(Author).filter(Author.id == author_id).first()

    def create(self, first_name: str, last_name: str) -> Author:
        author = Author(first_name=first_name, last_name=last_name)
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def update(self, author: Author, first_name: str | None, last_name: str | None) -> Author:
        if first_name is not None:
            author.first_name = first_name
        if last_name is not None:
            author.last_name = last_name
        self.db.commit()
        self.db.refresh(author)
        return author

    def delete(self, author: Author) -> None:
        self.db.delete(author)
        self.db.commit()