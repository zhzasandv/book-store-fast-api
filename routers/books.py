from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from repositories.book import BookRepository
from services.book import BookService
from schemas.book import BookDTO, BookCreateDTO, BookListDTO, BookUpdateDTO

router = APIRouter(prefix="/api/v1/books", tags=["books"])


def get_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(BookRepository(db))


@router.get("/", response_model=BookListDTO)
def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    q: str | None = Query(None, min_length=1),
    genre_id: int | None = Query(None, ge=1),
    author_id: int | None = Query(None, ge=1),
    service: BookService = Depends(get_service),
):
    return service.get_catalog(
        page=page,
        page_size=page_size,
        q=q,
        genre_id=genre_id,
        author_id=author_id,
    )


@router.get("/search", response_model=list[BookDTO])
def search_books(q: str = Query(..., min_length=1), service: BookService = Depends(get_service)):
    return service.search(q)


@router.get("/{book_id}", response_model=BookDTO)
def get_book(book_id: int, service: BookService = Depends(get_service)):
    return service.get_by_id(book_id)


@router.post("/", response_model=BookDTO, status_code=201)
def create_book(data: BookCreateDTO, service: BookService = Depends(get_service)):
    return service.create(data, service.repository.db)


@router.put("/{book_id}", response_model=BookDTO)
def update_book(book_id: int, data: BookUpdateDTO, service: BookService = Depends(get_service)):
    return service.update(book_id, data, service.repository.db)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, service: BookService = Depends(get_service)):
    service.delete(book_id)
