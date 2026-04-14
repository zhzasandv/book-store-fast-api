from fastapi import HTTPException
from repositories.book import BookRepository
from models.book import Author
from schemas.book import BookDTO, BookCreateDTO, BookListDTO, BookUpdateDTO
from sqlalchemy.orm import Session


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def _get_authors(self, db: Session, author_ids: list[int]) -> list[Author]:
        authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
        if len(authors) != len(author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")
        return authors

    def get_all(self) -> list[BookDTO]:
        return [BookDTO.model_validate(b) for b in self.repository.get_all()]

    def get_catalog(
        self,
        page: int,
        page_size: int,
        q: str | None = None,
        genre_id: int | None = None,
        author_id: int | None = None,
    ) -> BookListDTO:
        books, total = self.repository.get_catalog(
            page=page,
            page_size=page_size,
            q=q,
            genre_id=genre_id,
            author_id=author_id,
        )
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        return BookListDTO(
            items=[BookDTO.model_validate(b) for b in books],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def search(self, q: str) -> list[BookDTO]:
        return [BookDTO.model_validate(b) for b in self.repository.search(q)]

    def get_by_id(self, book_id: int) -> BookDTO:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookDTO.model_validate(book)

    def create(self, data: BookCreateDTO, db: Session) -> BookDTO:
        authors = self._get_authors(db, data.author_ids)
        book_data = data.model_dump(exclude={"author_ids"})
        book = self.repository.create(book_data, authors)
        return BookDTO.model_validate(book)

    def update(self, book_id: int, data: BookUpdateDTO, db: Session) -> BookDTO:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        authors = self._get_authors(db, data.author_ids) if data.author_ids is not None else None
        update_data = {k: v for k, v in data.model_dump(exclude={"author_ids"}).items() if v is not None}
        updated = self.repository.update(book, update_data, authors)
        return BookDTO.model_validate(updated)

    def delete(self, book_id: int) -> None:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        self.repository.delete(book)
