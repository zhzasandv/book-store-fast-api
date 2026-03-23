from repositories.author import AuthorRepository
from schemas.author import AuthorDTO


class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    def get_all(self) -> list[AuthorDTO]:
        authors = self.repository.get_all()
        return [AuthorDTO.model_validate(a) for a in authors]
