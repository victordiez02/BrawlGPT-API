"""
Este módulo importa funciones necesarias para la carga de datos, gestión de mapas.
"""
from google import genai
from scripts.functions import load_data, load_maps, print_draft_summary, generate_final_prompt, clean_console

clean_console()

# Carga los datos de los brawlers desde los archivos proporcionados.
# Devuelve un diccionario donde las claves son los nombres de los brawlers y los valores son objetos de la clase `Brawler`.
brawlers = load_data("meta/meta.txt", "meta/categories.txt", "meta/tier.txt")  # Dict[str, Brawler]

# Carga los mapas y sus características desde el archivo de mapas.
# Devuelve un diccionario donde las claves son los nombres de los mapas y los valores son objetos de la clase `Map`.
maps = load_maps("meta/maps.txt", brawlers)

selected_map = "Last Stop"  
phase = 3
banned_brawlers = ["Gus", "Sandy", "Chester", "Angelo"]
picks = ["Buster", "Darryl", "Bo"]
team = "red"

# Imprime en consola el resumen del draft con los picks y bans organizados en columnas.
# No devuelve nada (solo imprime).
print_draft_summary(selected_map, phase, team, banned_brawlers, picks)  # None (Solo imprime)

# Genera el archivo final con toda la información del draft.
# No devuelve nada, sino que guarda el archivo en la carpeta `final_prompt/`.
prompt = generate_final_prompt(phase, selected_map, maps, brawlers, banned_brawlers, team, picks, "data/prompts", "final_prompt")

cliente = genai.Client(api_key="AIzaSyD0PamArL9VXbx7zJ2cgj4-v9Wkhcoj7ns")

respuesta = cliente.models.generate_content(
    model='gemini-2.0-flash', contents=prompt
)

print(respuesta.text)
