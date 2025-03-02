from fastapi import APIRouter, HTTPException
from services.pokemon_service import PokemonService
from models.pokemon_models import PokemonModel

router = APIRouter(prefix="/api/pokemon", tags=["Pokemon"])
service = PokemonService()

@router.get("/saved")  # ✅ Primero se define esta ruta específica
async def get_saved_pokemon():
    return service.get_saved_pokemon()

@router.get("/{name}")  # ⬅️ Luego se define la búsqueda por nombre
async def get_pokemon(name: str):
    return service.get_pokemon(name)

@router.post("/save")
async def save_pokemon(pokemon: PokemonModel):
    return service.save_pokemon(pokemon.dict())

@router.get("/history")
async def get_history():
    return service.get_history()

@router.delete("/delete/{pokemon_id}/{rev}")
async def delete_pokemon(pokemon_id: str, rev: str):
    return service.delete_pokemon(pokemon_id, rev)

@router.put("/update/{pokemon_id}")
async def update_pokemon(pokemon_id: str, updated_pokemon: PokemonModel):
    return service.update_pokemon(pokemon_id, updated_pokemon)
