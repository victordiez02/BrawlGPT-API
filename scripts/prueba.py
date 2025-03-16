"""
Este módulo importa funciones necesarias para la carga de datos, gestión de mapas.
"""

import sys
import os

# Obtener la ruta del directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google import genai
from app.utils.config import load_data, load_maps, get_team, get_map, get_phase, clean_console
from app.services.draft_service import draft, execute_draft
from app.services.gemini_service import call_gemini

clean_console()

# Carga los datos de los brawlers desde los archivos proporcionados.
# Devuelve un diccionario donde las claves son los nombres de los brawlers y los valores son objetos de la clase `Brawler`.
brawlers = load_data("data/meta/mar2025/meta.txt", "data/meta/mar2025/categories.txt", "data/meta/mar2025/tier.txt")  # Dict[str, Brawler]

# Carga los mapas y sus características desde el archivo de mapas.
# Devuelve un diccionario donde las claves son los nombres de los mapas y los valores son objetos de la clase `Map`.
maps = load_maps("data/meta/mar2025/maps.txt", brawlers)  # Dict[str, Map]

# Solicita al usuario que seleccione un mapa de la lista de mapas disponibles.
# Devuelve un objeto de la clase `Map` correspondiente al mapa elegido.
selected_map = 'Sneaky Fields'  # Map

# Determina la fase actual del draft.
# Devuelve un entero que indica la fase (1 a 4).
phase = 3

# Determina qué equipo comienza el draft (azul o rojo).
# Devuelve una cadena con el nombre del equipo: "blue" o "red".
team = 'blue'  # str


# Realiza el proceso de draft en función de la fase y el equipo actual.
# Devuelve dos listas:
# - `banned_brawlers`: Lista de strings con los nombres de los brawlers baneados.
# - `picks`: Lista de strings con los nombres de los brawlers seleccionados en el draft.
banned_brawlers = ['Ollie', 'Sandy', 'Kenji']
picks = ["Bea", "Barley", "Rico"]

# Ejecutar el proceso de draft usando execute_draft
# Devuelve un diccionario con el resumen del draft y el prompt generado para la IA.
draft_data = execute_draft(phase, selected_map, maps, brawlers, banned_brawlers, team, picks)

# Genera el archivo final con toda la información del draft.
# No devuelve nada, sino que guarda el archivo en la carpeta `final_prompt/`.
prompt = draft_data["prompt"]

# Obtener respuesta de Gemini
# Llama a `call_gemini()` que envía el prompt a la IA y recibe una respuesta con las mejores opciones, imprimiendola por pantalla.
gemini_response = call_gemini(draft_data["prompt"])

