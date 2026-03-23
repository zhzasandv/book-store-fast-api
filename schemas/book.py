from pydantic import BaseModel, computed_field
from typing import Optional
from schemas.author import AuthorDTO
from schemas.genre import GenreDTO
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class BookDTO(BaseModel):
    id: int
    name: str
    price: float
    title: str
    publication_date: str
    genre: GenreDTO
    authors: list[AuthorDTO]
    oblojka: Optional[str] = None

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.oblojka:
            return f"{BASE_URL}/media/{self.oblojka}"
        return None

    model_config = {"from_attributes": True}
