"""
Este módulo importa funciones necesarias para la carga de datos, gestión de mapas.
"""

import sys
import os

# Obtener la ruta del directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.config import load_data, load_maps, get_team, get_map, get_phase, clean_console, generate_final_prompt
from app.services.draft_service import draft
from app.services.gemini_service import call_gemini
from app.services.draft_service import print_draft_summary

clean_console()

# Carga los datos de los brawlers desde los archivos proporcionados.
# Devuelve un diccionario donde las claves son los nombres de los brawlers y los valores son objetos de la clase `Brawler`.
brawlers = load_data("data/meta/mar2025/meta.txt", "data/meta/mar2025/categories.txt", "data/meta/mar2025/tier.txt")  # Dict[str, Brawler]

# Carga los mapas y sus características desde el archivo de mapas.
# Devuelve un diccionario donde las claves son los nombres de los mapas y los valores son objetos de la clase `Map`.
maps = load_maps("data/meta/mar2025/maps.txt", brawlers)  # Dict[str, Map]

# Solicita al usuario que seleccione un mapa de la lista de mapas disponibles.
# Devuelve un objeto de la clase `Map` correspondiente al mapa elegido.
selected_map = get_map(maps)  # Map

# Determina la fase actual del draft.
# Devuelve un entero que indica la fase (1 a 4).
phase = get_phase()  # int

# Determina qué equipo comienza el draft (azul o rojo).
# Devuelve una cadena con el nombre del equipo: "blue" o "red".
team = get_team()  # str


# Realiza el proceso de draft en función de la fase y el equipo actual.
# Devuelve dos listas:
# - `banned_brawlers`: Lista de strings con los nombres de los brawlers baneados.
# - `picks`: Lista de strings con los nombres de los brawlers seleccionados en el draft.
[banned_brawlers, picks] = draft(phase, team, brawlers)  # List[str], List[str]

# Ejecutar el proceso de draft usando generate_final_prompt
# Devuelve el archivo final con toda la información del draft generado para la IA.
prompt = generate_final_prompt(phase, selected_map, maps, brawlers, banned_brawlers, team, picks)

# Imprimir resumen del draft
print_draft_summary(phase, team, banned_brawlers, picks, brawlers)

# Obtener respuesta de Gemini
# Llama a `call_gemini()` que envía el prompt a la IA y recibe una respuesta con las mejores opciones, imprimiendola por pantalla.
gemini_response = call_gemini(prompt)

