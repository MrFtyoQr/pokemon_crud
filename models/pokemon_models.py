from pydantic import BaseModel
from typing import List, Optional

class PokemonModel(BaseModel):
    name: str
    height: int
    weight: int
    types: List[str]  
    abilities: List[str]  

class PokemonResponse(PokemonModel):
    id: Optional[str]
    rev: Optional[str]
