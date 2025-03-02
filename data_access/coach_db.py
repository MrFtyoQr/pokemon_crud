 
import requests


class CouchDB:
    def __init__(self, db_url: str = "http://127.0.0.1:5984", user: str = "joseph", password: str = "54321"):
        self.db_url = db_url
        self.auth = (user, password)
        self.pokemon_db = "crud-pokemon"
        self.history_db = "historico-crud"

    def save_pokemon(self, pokemon: dict):
        response = requests.post(f"{self.db_url}/{self.pokemon_db}", json=pokemon, auth=self.auth)
        return response.json()

    def save_history(self, pokemon: dict):
        response = requests.post(f"{self.db_url}/{self.history_db}", json=pokemon, auth=self.auth)
        return response.json()

    def get_saved_pokemon(self):
        response = requests.get(f"{self.db_url}/{self.pokemon_db}/_all_docs?include_docs=true", auth=self.auth)
        print("🔍 Respuesta de CouchDB:", response.json())  # 🔍 DEBUG

        if response.status_code != 200:
            print("❌ Error al obtener los Pokémon guardados:", response.text)
            return []

        docs = response.json().get("rows", [])
        return [doc["doc"] for doc in docs]
    
    def get_pokemon_by_id(self, pokemon_id: str):
        response = requests.get(f"{self.db_url}/{self.pokemon_db}/{pokemon_id}", auth=self.auth)
        
        if response.status_code != 200:
            print(f"❌ Error al obtener el Pokémon con ID {pokemon_id}: {response.text}")  # 🔍 Debug
            return None

        return response.json()





    def delete_pokemon(self, pokemon_id: str, rev: str):
        response = requests.delete(f"{self.db_url}/{self.pokemon_db}/{pokemon_id}?rev={rev}", auth=self.auth)
        return response.json()
    
    def update_pokemon(self, pokemon: dict):
        response = requests.put(f"{self.db_url}/{self.pokemon_db}/{pokemon['_id']}", json=pokemon, auth=self.auth)
        return response.json()

