from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories.genre import GenreRepository
from services.genre import GenreService
from schemas.genre import GenreDTO

router = APIRouter(prefix="/api/v1/genres", tags=["genres"])


def get_service(db: Session = Depends(get_db)) -> GenreService:
    return GenreService(GenreRepository(db))


@router.get("/", response_model=list[GenreDTO])
def get_genres(service: GenreService = Depends(get_service)):
    return service.get_all()
