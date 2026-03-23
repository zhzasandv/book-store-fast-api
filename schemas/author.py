from pydantic import BaseModel


class AuthorDTO(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}


class AuthorCreateDTO(BaseModel):
    first_name: str
    last_name: str


class AuthorUpdateDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None