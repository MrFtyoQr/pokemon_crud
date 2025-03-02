import logging
from data_access.coach_db import CouchDB
from fastapi import HTTPException
from models.pokemon_models import PokemonModel
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PokemonService:
    def __init__(self):
        self.db = CouchDB()
        self.base_url = "https://pokeapi.co/api/v2/pokemon"

    def get_pokemon(self, name: str):
        logging.info(f"Buscando Pokémon: {name}")  # ✅ Reemplazo de print por logging
        response = requests.get(f"{self.base_url}/{name}")
        if response.status_code != 200:
            logging.error(f"Error al obtener el Pokémon: {response.status_code}")  # ✅ Logging en caso de error
            raise HTTPException(status_code=404, detail="Pokemon not found")
        
        data = response.json()
        pokemon_info = {
            "name": data.get("name"),
            "height": data.get("height"),
            "weight": data.get("weight"),
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
        }

        self.db.save_history(pokemon_info)
        return pokemon_info

    def save_pokemon(self, pokemon: dict):
        return self.db.save_pokemon(pokemon)

    def get_saved_pokemon(self):
        saved_pokemon = self.db.get_saved_pokemon()
        logging.info(f"✅ Pokémon guardados en la BD: {saved_pokemon}")  # ✅ Logging en lugar de print

        if not saved_pokemon:
            logging.warning("No saved Pokémon found")  # ✅ Logging de advertencia si no hay datos
            raise HTTPException(status_code=404, detail="No saved Pokémon found")

        return saved_pokemon

    def get_history(self):
        return self.db.get_history()

    def delete_pokemon(self, pokemon_id: str, rev: str):
        return self.db.delete_pokemon(pokemon_id, rev)

    def update_pokemon(self, pokemon_id: str, updated_pokemon: PokemonModel):
        pokemon_data = self.db.get_pokemon_by_id(pokemon_id)
        if not pokemon_data:
            logging.error(f"Pokemon con ID {pokemon_id} no encontrado para actualizar")  # ✅ Logging de error
            raise HTTPException(status_code=404, detail="Pokemon not found")

        updated_pokemon_dict = updated_pokemon.dict()
        updated_pokemon_dict["_id"] = pokemon_id
        updated_pokemon_dict["_rev"] = pokemon_data["_rev"]

        logging.info(f"Actualizando Pokémon con ID {pokemon_id}")  # ✅ Logging de actualización
        return self.db.update_pokemon(updated_pokemon_dict)