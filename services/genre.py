from fastapi import HTTPException
from repositories.genre import GenreRepository
from schemas.genre import GenreDTO, GenreCreateDTO, GenreUpdateDTO


class GenreService:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def get_all(self) -> list[GenreDTO]:
        return [GenreDTO.model_validate(g) for g in self.repository.get_all()]

    def get_by_id(self, genre_id: int) -> GenreDTO:
        genre = self.repository.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return GenreDTO.model_validate(genre)

    def create(self, data: GenreCreateDTO) -> GenreDTO:
        genre = self.repository.create(data.name)
        return GenreDTO.model_validate(genre)

    def update(self, genre_id: int, data: GenreUpdateDTO) -> GenreDTO:
        genre = self.repository.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        updated = self.repository.update(genre, data.name)
        return GenreDTO.model_validate(updated)

    def delete(self, genre_id: int) -> None:
        genre = self.repository.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        self.repository.delete(genre)