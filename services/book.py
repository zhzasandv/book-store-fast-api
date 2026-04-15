from fastapi import HTTPException
from repositories.book import BookRepository
from models.book import Author
from schemas.book import BookDTO, BookCreateDTO, BookListDTO, BookUpdateDTO


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def _get_authors(self, author_ids: list[int]) -> list[Author]:
        unique_author_ids = set(author_ids)
        authors = self.repository.get_authors_by_ids(author_ids)
        if len(authors) != len(unique_author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")
        return authors

    def _ensure_genre_exists(self, genre_id: int) -> None:
        if not self.repository.genre_exists(genre_id):
            raise HTTPException(status_code=404, detail="Genre not found")

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

    def create(self, data: BookCreateDTO) -> BookDTO:
        self._ensure_genre_exists(data.genre_id)
        authors = self._get_authors(data.author_ids)
        book_data = data.model_dump(exclude={"author_ids"})
        book = self.repository.create(book_data, authors)
        return BookDTO.model_validate(book)

    def update(self, book_id: int, data: BookUpdateDTO) -> BookDTO:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if data.genre_id is not None:
            self._ensure_genre_exists(data.genre_id)

        authors = self._get_authors(data.author_ids) if data.author_ids is not None else None
        update_data = {
            key: value
            for key, value in data.model_dump(exclude={"author_ids"}).items()
            if value is not None
        }
        updated = self.repository.update(book, update_data, authors)
        return BookDTO.model_validate(updated)

    def delete(self, book_id: int) -> None:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        self.repository.delete(book)
