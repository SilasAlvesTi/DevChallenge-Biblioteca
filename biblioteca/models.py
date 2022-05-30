from itertools import count
from typing import List, Optional

from pydantic import BaseModel, Field
c = count()


class Obra(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    titulo: str
    editora: str
    foto: str
    autores: List[str]


class Biblioteca(BaseModel):
    biblioteca: List[Obra]
    count: int
