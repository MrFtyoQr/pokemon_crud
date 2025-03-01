from pydantic import BaseModel
from typing import List, Optional

class PokemonModel(BaseModel):
    name: str
    height: int
    weight: int
    types: List[str]  # ✅ Asegurar que se recibe una lista
    abilities: List[str]  # ✅ Asegurar que se recibe una lista

class PokemonResponse(PokemonModel):
    id: Optional[str]
    rev: Optional[str]
