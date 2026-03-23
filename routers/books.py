from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories.book import BookRepository
from services.book import BookService
from schemas.book import BookDTO

router = APIRouter(prefix="/api/v1/books", tags=["books"])


def get_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(BookRepository(db))


@router.get("/", response_model=list[BookDTO])
def get_books(service: BookService = Depends(get_service)):
    return service.get_all()
