from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from database import get_db
from repositories.genre import GenreRepository
from services.genre import GenreService
from schemas.genre import GenreDTO, GenreCreateDTO, GenreUpdateDTO

router = APIRouter(prefix="/api/v1/genres", tags=["genres"])


def get_service(db: Session = Depends(get_db)) -> GenreService:
    return GenreService(GenreRepository(db))


@router.get("/", response_model=list[GenreDTO])
def get_genres(service: GenreService = Depends(get_service)):
    return service.get_all()


@router.get("/{genre_id}", response_model=GenreDTO)
def get_genre(genre_id: int, service: GenreService = Depends(get_service)):
    return service.get_by_id(genre_id)


@router.post("/", response_model=GenreDTO, status_code=201)
def create_genre(data: GenreCreateDTO, service: GenreService = Depends(get_service)):
    return service.create(data)


@router.put("/{genre_id}", response_model=GenreDTO)
def update_genre(genre_id: int, data: GenreUpdateDTO, service: GenreService = Depends(get_service)):
    return service.update(genre_id, data)


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, service: GenreService = Depends(get_service)):
    service.delete(genre_id)