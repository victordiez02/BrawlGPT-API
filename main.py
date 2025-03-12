"""
Este script define una API en FastAPI para gestionar un sistema de draft en Brawl Stars.

Características:
- Carga los datos de brawlers y mapas desde archivos de texto al iniciar la API.
- Define la estructura de la API y registra las rutas desde `draft_routes.py`.
- Usa `app.state` para almacenar `maps` y `brawlers` y hacerlos accesibles globalmente.
- Permite recibir información de la fase actual del draft, el equipo que elige, los bans y picks previos.
- Gestiona la lógica del draft y envía los datos a la API de Gemini para obtener recomendaciones.

Rutas disponibles:
- `POST /draft`: Recibe datos del draft y devuelve el resumen del draft junto con la recomendación de Gemini.

Requiere una clave API de Gemini para funcionar correctamente.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.draft_routes import router as draft_router
from app.utils.config import load_data, load_maps
from contextlib import asynccontextmanager

# Cargar los datos al iniciar la API (solo una vez)
brawlers = load_data("data/meta/meta.txt", "data/meta/categories.txt", "data/meta/tier.txt")
maps = load_maps("data/meta/maps.txt", brawlers)

# Inicializar la aplicación FastAPI
app = FastAPI()

@asynccontextmanager
async def lifespan():
    print("API Version: 1.0.0")  # Mensaje de versión al iniciar
    yield
    print("Shutting down...")  # Mensaje al cerrar la API (opcional)

# Añadir el Lifespan Event a la aplicación
app.state.lifespan = lifespan

# Configuración de CORS para permitir solo el método GET
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen.
    allow_credentials=True,
    allow_methods=["GET"],  # Permite solo el método GET
    allow_headers=["*"],  # Permite cualquier header
)

# Almacenar `brawlers` y `maps` en `app.state` para que estén disponibles globalmente
app.state.brawlers = brawlers
app.state.maps = maps

# Registrar las rutas de la API
app.include_router(draft_router)
