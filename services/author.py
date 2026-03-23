from fastapi import HTTPException
from repositories.author import AuthorRepository
from schemas.author import AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO


class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    def get_all(self) -> list[AuthorDTO]:
        authors = self.repository.get_all()
        return [AuthorDTO.model_validate(a) for a in authors]

    def get_by_id(self, author_id: int) -> AuthorDTO:
        author = self.repository.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorDTO.model_validate(author)

    def create(self, data: AuthorCreateDTO) -> AuthorDTO:
        author = self.repository.create(data.first_name, data.last_name)
        return AuthorDTO.model_validate(author)

    def update(self, author_id: int, data: AuthorUpdateDTO) -> AuthorDTO:
        author = self.repository.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        updated = self.repository.update(author, data.first_name, data.last_name)
        return AuthorDTO.model_validate(updated)

    def delete(self, author_id: int) -> None:
        author = self.repository.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        self.repository.delete(author)