from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories.author import AuthorRepository
from services.author import AuthorService
from schemas.author import AuthorDTO

router = APIRouter(prefix="/api/v1/authors", tags=["authors"])


def get_service(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(AuthorRepository(db))


@router.get("/", response_model=list[AuthorDTO])
def get_authors(service: AuthorService = Depends(get_service)):
    return service.get_all()
