import requests
from data_access.coach_db import CouchDB
from fastapi import HTTPException

class PokemonService:
    def __init__(self):
        self.db = CouchDB()
        self.base_url = "https://pokeapi.co/api/v2/pokemon"

    def get_pokemon(self, name: str):
        print(f"Buscando Pokémon: {name}")  # DEBUG
        response = requests.get(f"{self.base_url}/{name}")
        if response.status_code != 200:
            print(f"Error al obtener el Pokémon: {response.status_code}")  # DEBUG
            raise HTTPException(status_code=404, detail="Pokemon not found")
        
        data = response.json()
        pokemon_info = {
            "name": data.get("name"),
            "height": data.get("height"),
            "weight": data.get("weight"),
            "types": [t["type"]["name"] for t in data["types"]],  # ✅ Se agregó types
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
        }

        self.db.save_history(pokemon_info)
        return pokemon_info

    def save_pokemon(self, pokemon: dict):
        return self.db.save_pokemon(pokemon)

    def get_saved_pokemon(self):
        saved_pokemon = self.db.get_saved_pokemon()
        print("Pokémon guardados en BD:", saved_pokemon)  # 🔍 DEBUG
        if not saved_pokemon:
            raise HTTPException(status_code=404, detail="No saved Pokémon found")
        return saved_pokemon


    def get_history(self):
        return self.db.get_history()

    def delete_pokemon(self, pokemon_id: str, rev: str):
        return self.db.delete_pokemon(pokemon_id, rev)

    def update_pokemon(self, pokemon_id: str, updated_pokemon: dict):
        pokemon_data = self.db.get_pokemon_by_id(pokemon_id)
        if not pokemon_data:
            raise HTTPException(status_code=404, detail="Pokemon not found")

        updated_pokemon["_id"] = pokemon_id  # Mantener el mismo ID
        updated_pokemon["_rev"] = pokemon_data["_rev"]  # Mantener la revisión correcta

        return self.db.update_pokemon(updated_pokemon)
