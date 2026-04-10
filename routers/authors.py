from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from database import get_db
from repositories.author import AuthorRepository
from services.author import AuthorService
from schemas.author import AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO

router = APIRouter(prefix="/api/v1/authors", tags=["authors"])


def get_service(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(AuthorRepository(db))


@router.get("/", response_model=list[AuthorDTO])
def get_authors(service: AuthorService = Depends(get_service)):
    return service.get_all()


@router.get("/{author_id}", response_model=AuthorDTO)
def get_author(author_id: int, service: AuthorService = Depends(get_service)):
    return service.get_by_id(author_id)


@router.post("/", response_model=AuthorDTO, status_code=201)
def create_author(data: AuthorCreateDTO, service: AuthorService = Depends(get_service)):
    return service.create(data)


@router.put("/{author_id}", response_model=AuthorDTO)
def update_author(author_id: int, data: AuthorUpdateDTO, service: AuthorService = Depends(get_service)):
    return service.update(author_id, data)


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, service: AuthorService = Depends(get_service)):
    service.delete(author_id)