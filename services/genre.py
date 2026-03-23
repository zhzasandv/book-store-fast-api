from repositories.genre import GenreRepository
from schemas.genre import GenreDTO


class GenreService:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def get_all(self) -> list[GenreDTO]:
        genres = self.repository.get_all()
        return [GenreDTO.model_validate(g) for g in genres]
