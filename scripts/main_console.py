"""
Este módulo importa funciones necesarias para la carga de datos, gestión de mapas.
"""

from google import genai
# from functions import load_maps, get_team, get_map, get_phase, draft, print_draft_summary, generate_final_prompt, clean_console
from app.utils.config import load_data, load_maps, get_team, get_map, get_phase, generate_final_prompt, clean_console
from app.services.draft_service import draft, print_draft_summary


clean_console()

# Carga los datos de los brawlers desde los archivos proporcionados.
# Devuelve un diccionario donde las claves son los nombres de los brawlers y los valores son objetos de la clase `Brawler`.
brawlers = load_data("data/meta/meta.txt", "data/meta/categories.txt", "data/meta/tier.txt")  # Dict[str, Brawler]

# Carga los mapas y sus características desde el archivo de mapas.
# Devuelve un diccionario donde las claves son los nombres de los mapas y los valores son objetos de la clase `Map`.
maps = load_maps("data/meta/maps.txt", brawlers)  # Dict[str, Map]

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

# Imprime en consola el resumen del draft con los picks y bans organizados en columnas.
# No devuelve nada (solo imprime).
print_draft_summary(selected_map, phase, team, banned_brawlers, picks)  # None (Solo imprime)

# Genera el archivo final con toda la información del draft.
# No devuelve nada, sino que guarda el archivo en la carpeta `final_prompt/`.
prompt = generate_final_prompt(phase, selected_map, maps, brawlers, banned_brawlers, team, picks, "data/prompts", "final_prompt")


# Inicialización del cliente para interactuar con el modelo Gemini de Google AI.
# Requiere una clave API para autenticación.
client = genai.Client(api_key="AIzaSyD0PamArL9VXbx7zJ2cgj4-v9Wkhcoj7ns")

# Utiliza el cliente para generar contenido a partir del prompt creado.
# 'gemini-2.0-flash' es el modelo específico de Gemini que se utilizará.
# 'prompt' contiene toda la información del draft necesaria para que Gemini genere la respuesta.
response = client.models.generate_content(
    model='gemini-2.0-flash', contents=prompt
)

# Imprime la respuesta generada por Gemini en la consola.
# 'response.text' contiene el texto de la respuesta del modelo.
print("BEST OPTIONS:")
print(response.text)
