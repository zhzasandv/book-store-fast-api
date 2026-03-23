from repositories.book import BookRepository
from schemas.book import BookDTO


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_all(self) -> list[BookDTO]:
        books = self.repository.get_all()
        return [BookDTO.model_validate(b) for b in books]
