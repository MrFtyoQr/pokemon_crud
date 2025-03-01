from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.pokemon import router as pokemon_router
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Pokemon CRUD API", description="API para gestionar Pokémon con CouchDB", version="1.0")
app.include_router(pokemon_router, prefix="/api")  # Eliminar el prefijo adicional

# Servir archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
async def read_history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})
