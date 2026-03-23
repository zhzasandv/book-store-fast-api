from pydantic import BaseModel


class GenreDTO(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
