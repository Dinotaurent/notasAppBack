from pydantic import BaseModel, Field
from typing import Optional


class Nota(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3)
    contenido: Optional[str] = Field(default=None, min_length=6)
