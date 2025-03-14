"""
Módulo de configuración y utilidades generales para el sistema de draft.

Funciones:
- clean_console(): Limpia la consola dependiendo del sistema operativo.
- load_brawlers(archive): Carga los brawlers desde un archivo de texto.
- load_categories(archive, brawlers): Carga las categorías de los brawlers.
- assign_counters(archive, brawlers, categories): Asigna los counters de cada brawler.
- assign_tier(tier_file, brawlers): Asigna el tier de cada brawler.
- load_data(meta, categories, tier): Carga toda la información de los brawlers en un diccionario.
- load_maps(file_path, brawlers): Carga los mapas con sus características y brawlers recomendados.
- load_brawlers_from_file(file_path): Carga solo los nombres de los brawlers en una lista.
- get_team(): Obtiene el equipo que comienza el draft.
- get_map(maps_dict): Obtiene el mapa seleccionado.
- get_phase(): Obtiene la fase del draft actual.
- complete(text, state): Autocompleta nombres de brawlers.
- get_draft_summary(phase, team, banned_brawlers, picks, brawlers): Genera un resumen del draft para la IA.
- generate_final_prompt(phase, selected_map, maps, brawlers, banned_brawlers, team, picks, "prompts", "final_prompt"): Genera un archivo final con el prompt completo para la IA.
"""
import os
from termcolor import colored
from app.models.classes import Brawler, Map
#from app.services.draft_service import get_draft_summary

# Función para limpiar la consola
def clean_console():
    """Función para limpiar consola."""
    # Verificamos el sistema operativo y ejecutamos el comando correspondiente
    if os.name == 'posix':  # Linux o macOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')

# Paso 1: Crear brawlers desde meta.txt (solo los nombres)
def load_brawlers(archive):
    """Función para cargar los brawlers."""
    brawlers = {}

    with open(archive, 'r', encoding='utf-8') as file:
        for line in file:
            # Limpiar la línea y separar el nombre del brawler (antes de los dos puntos)
            line = line.strip()
            name = line.split(": ")[0]
            brawlers[name.strip()] = Brawler(name.strip())

    return brawlers

# Paso 2: Crear los conjuntos de tipos de brawlers desde categories.txt
def load_categories(archive, brawlers):
    """Función para cargar las categorías."""
    categories = {}

    with open(archive, 'r', encoding='utf-8') as file:
        for line in file:
            # Limpiar la línea y separar la categoría de los brawlers
            line = line.strip()
            if not line:  # Saltar líneas vacías
                continue

            category, brawlers_list = line.split(":")
            category = category.strip()
            brawlers_list = [b.strip() for b in brawlers_list.split("|")]

            # Inicializar la categoría si no existe
            if category not in categories:
                categories[category] = []

            # Agregar solo los nombres de los brawlers si existen en el diccionario brawlers
            for brawler_name in brawlers_list:
                if brawler_name in brawlers:
                    categories[category].append(brawler_name)

    return categories


# Paso 3: Asignar los counters desde meta.txt, incluyendo los tipos de brawlers
def assign_counters(archive, brawlers, categories):
    """Función para asignar a cada brawler sus counters."""
    with open(archive, 'r', encoding='utf-8') as file:
        for line in file:
            # Limpiar la línea y dividir en nombre del brawler y sus counters
            line = line.strip()
            name, counters = line.split(": ")
            name = name.strip()
            counters = counters.split("|")  # Separar los counters por "|"

            # Verificar si el brawler ya existe
            if name in brawlers:
                brawler = brawlers[name]
                for counter_name in counters:
                    counter_name = counter_name.strip()

                    # Si el counter es un brawler, lo agregamos
                    if counter_name in brawlers:
                        brawler.add_counter(brawlers[counter_name])
                    # Si el counter es una categoría, agregamos todos los brawlers de esa categoría
                    elif counter_name in categories:
                        for counter_brawler_name in categories[counter_name]:
                            if counter_brawler_name in brawlers:
                                brawler.add_counter(brawlers[counter_brawler_name])

    return brawlers

def assign_tier(tier_file, brawlers):
    """Función para asignar a cada brawler su tier."""
    with open(tier_file, 'r', encoding='utf-8')  as file:
        for line in file:
            line = line.strip()
            tier, brawlers_list = line.split(": ")
            brawlers_list = brawlers_list.split("|")
            for brawler_name in brawlers_list:
                brawler_name = brawler_name.strip()
                if brawler_name in brawlers:
                    brawlers[brawler_name].tier = tier  # Asignar el tier a cada brawler
    return brawlers

# Función principal para cargar todos los datos
def load_data(meta, categories, tier):
    """Función para cargar toda la información en los diccionarios brawlers y maps."""
    # Cargar los brawlers desde meta.txt
    brawlers = load_brawlers(meta)

    # Cargar los tipos desde categories.txt
    categories_list = load_categories(categories, brawlers)

    # Asignar los counters
    brawlers = assign_counters(meta, brawlers, categories_list)

    # Asignar los tiers desde tier.txt
    brawlers = assign_tier(tier, brawlers)

    return brawlers

def load_maps(file_path, brawlers):
    """Función para cargar todos los mapas de maps.txt."""
    maps = {}
    with open(file_path, 'r', encoding='utf-8')  as file:
        lines = file.readlines()

    current_map = None
    map_name = None

    for line in lines:
        line = line.strip()

        if not line:
            continue  # Saltar líneas vacías
        # Si encontramos el nombre del mapa (línea que no tiene - o algo más después de : )
        if ":" in line and not line.startswith("-"):
            map_name = line.split(":")[0].strip()  # Extraer el nombre del mapa
            current_map = Map(name=map_name, mode="", has_indestructible_walls=False)
            maps[map_name] = current_map  # Guardar el mapa en el diccionario
        elif line.startswith("- Mode:"):
            current_map.mode = line.split(":")[1].strip()
        elif line.startswith("- Has indestructive walls:"):
            current_map.has_indestructible_walls = line.split(":")[1].strip().lower() == "yes"
        elif line.startswith("- 1st Pick:"):
            # Obtener las referencias de los brawlers usando los nombres
            first_picks = line.split(":")[1].strip().split(" | ")
            current_map.first_pick = [
                brawlers[name.strip()] for name in first_picks if name.strip() in brawlers
            ]
        elif line.startswith("- Last Pick:"):
            last_picks = line.split(":")[1].strip().split(" | ")
            current_map.last_pick = [
                brawlers[name.strip()] for name in last_picks if name.strip() in brawlers
            ]
        elif line.startswith("- Other Picks:"):
            other_picks = line.split(":")[1].strip().split(" | ")
            current_map.other_picks = [
                brawlers[name.strip()] for name in other_picks if name.strip() in brawlers
            ]
        elif line.startswith("- Mid:"):
            current_map.mid = line.split(":")[1].strip()
        elif line.startswith("- Lane:"):
            current_map.lane = line.split(":")[1].strip()
        elif line.startswith("- Estrategy:"):
            current_map.strategy = line.split(":")[1].strip()

    return maps


def load_brawlers_from_file(file_path):
    """Función para cargar solo los nombres de los brawlers en una lista"""
    brawlers = []
    with open(file_path, 'r', encoding='utf-8')  as file:
        for line in file:
            # Extraer el nombre del brawler antes de los dos puntos
            brawler_name = line.split(":")[0].strip()
            brawlers.append(brawler_name)
    return brawlers

def get_team():
    """Recoge el equipo que empieza eligiendo y el mapa seleccionado, con el diccionario de mapas."""
    valid_teams = ['blue', 'red']  # Valid teams

    team_completed = False
    while not team_completed:
        print(f"Which team starts picking? ({colored('Blue', 'blue')}/{colored('Red', 'red')}):")
        team = input().strip().lower()  # Read input and convert to lowercase to normalize
        if team in valid_teams:  # Check if the response is valid
            team_completed = True
            clean_console()
        else:
            clean_console()
            print(f"Invalid team name. Please enter {colored('Blue', 'blue')} or {colored('Red', 'red')}.")
    return team

def get_map(maps_dict):
    """Recoge el mapa seleccionado, con el diccionario de mapas."""
    map_completed = False
    selected_map = None
    while not map_completed:
        print("\nWhich map has been selected? (enter the name of the map):")
        print("\nAvailable maps:")
        for map_name, map_obj in maps_dict.items():
            print(f"{map_name} ({map_obj.mode})")  # Print map name and its game mode

        map_name = input().strip()  # Read input

        # Check if the map exists in the dictionary
        if map_name in maps_dict:
            selected_map = maps_dict[map_name]
            map_completed = True
            clean_console()
        else:
            clean_console()
            print(f"'{map_name}' is not a valid map. Please choose a valid map.")

    return selected_map.name

def get_phase():
    """Obtiene la fase del draft, pidiendo un número del 1 al 4 con explicaciones claras."""
    phase_completed = False
    while not phase_completed:
        print(f"Please enter the draft phase ({colored('1', 'cyan')}-{colored('4', 'cyan')}) based on your current stage:")
        print(f"{colored('1', 'cyan')}: First phase - Choose the 1st pick. This is the first pick of the draft.")
        print(f"{colored('2', 'cyan')}: Second phase - Choose the 2nd and 3rd picks. This is the second part of the draft.")
        print(f"{colored('3', 'cyan')}: Third phase - Choose the 4th and 5th picks. This is the third part of the draft.")
        print(f"{colored('4', 'cyan')}: Fourth phase - Choose the last pick. This is the final pick of the draft.")

        # Solicitar al usuario el número de la fase
        phase = input("Enter the phase number (1-4): ").strip()

        # Verificar si la entrada es un número entero entre 1 y 4
        if phase.isdigit() and int(phase) in [1, 2, 3, 4]:
            phase_completed = True
            clean_console()
        else:
            clean_console()
            print("Invalid input! Please enter a valid integer between 1 and 4.")

    return int(phase)

def complete(text, state):
    """Función de autocompletado para readline."""
    brawlers = load_brawlers_from_file('meta.txt')
    options = [brawler for brawler in brawlers if brawler.lower().startswith(text.lower())]
    return options[state] if state < len(options) else None

def get_draft_summary(phase, team, banned_brawlers, picks, brawlers):
    """Genera un string optimizado para la IA con el resumen del draft, que se añadirá al prompt."""

    summary = []
    summary.append("CURRENT DRAFT")

    # Determinar el equipo que comenzó el draft y el equipo que elige segundo
    first_pick_team = "Blue" if team == "blue" else "Red"
    second_pick_team = "Red" if team == "blue" else "Blue"

    summary.append(f"First Pick Team: {first_pick_team}")
    summary.append(f"Second Pick Team: {second_pick_team}")

    summary.append(f"\nPhase {phase}")

    # Determinar el equipo que elige en este turno
    if phase % 2:  # Fase impar → elige el equipo que comenzó
        next_turn = "BLUE" if team == "blue" else "RED"
    else:  # Fase par → elige el equipo contrario
        next_turn = "RED" if team == "blue" else "BLUE"

    # Explicación del turno actual para la IA
    turn_explanation = {
        1: f"{next_turn} Team (my team) is choosing the First Pick, so make the optimal prediction.",
        2: f"{next_turn} Team (my team) is choosing the 2nd and 3rd Picks, so make the optimal prediction.",
        3: f"{next_turn} Team (my team) is choosing the 4th and 5th Picks, so make the optimal prediction.",
        4: f"{next_turn} Team (my team) is choosing the Last Pick, so make the optimal prediction."
    }

    summary.append(f"NEXT TURN: {turn_explanation[phase]}")

    # Añadir brawlers baneados
    summary.append("Banned Brawlers: " + (", ".join(banned_brawlers) if banned_brawlers else "None"))

    # Determinar los picks de cada equipo según quién comenzó
    # Determinar los picks de cada equipo según quién comenzó
    if team == "blue":
        first_pick_team_picks = [picks[0] if len(picks) > 0 else "---", picks[3] if len(picks) > 3 else "---", picks[4] if len(picks) > 4 else "---"]
        second_pick_team_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", picks[5] if len(picks) > 5 else "---"]
    else:
        first_pick_team_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", picks[5] if len(picks) > 5 else "---"]
        second_pick_team_picks = [picks[0] if len(picks) > 0 else "---", picks[3] if len(picks) > 3 else "---", picks[4] if len(picks) > 4 else "---"]

    # Etiquetas para mayor claridad en la IA
    enemy_team_label = f" {first_pick_team.upper()} TEAM (ENEMIES):"
    my_team_label = f" {second_pick_team.upper()} TEAM (MY TEAM):"

    # Modificar los picks según la fase
    if phase == 1:
        first_pick_team_picks = ["(Pick here)", "---", "---"]
        second_pick_team_picks = ["---", "---", "---"]

    elif phase == 2:
        first_pick_team_picks = [picks[0] if len(picks) > 0 else "---", "---", "---"]
        second_pick_team_picks = ["(Pick here)", "(Pick here)", "---"]

    elif phase == 3:
        first_pick_team_picks = [picks[0] if len(picks) > 0 else "---", "(Pick here)", "(Pick here)"]
        second_pick_team_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", "---"]

    elif phase == 4:
        first_pick_team_picks = [picks[0] if len(picks) > 0 else "---", picks[3] if len(picks) > 3 else "---", picks[4] if len(picks) > 4 else "---"]
        second_pick_team_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", "(Pick here)"]

    # Construcción del resumen
    summary.append(f"\n{enemy_team_label}")
    for pick in first_pick_team_picks:
        summary.append(f"- {pick}")

    summary.append(f"\n{my_team_label}")
    for pick in second_pick_team_picks:
        summary.append(f"- {pick}")

    # Decir los counters de los brawlers enemigos
    if picks:
        summary.append("\nCOUNTERS OF ENEMY BRAWLERS (consider this when picking):")
        enemy_picks = []
        if phase == 2:
            enemy_picks = [picks[0]] if len(picks) > 0 else []
        elif phase == 3:
            enemy_picks = [picks[1], picks[2]] if len(picks) > 2 else picks[1:len(picks)]
        elif phase == 4:
            enemy_picks = [picks[0], picks[3], picks[4]] if len(picks) > 4 else [picks[0]] + picks[3:len(picks)]

        for pick in enemy_picks:
            if pick in brawlers:
                counters_str = ", ".join([counter.name for counter in brawlers[pick].counters])
                summary.append(f"{pick} is countered by {counters_str}.")
            else:
                summary.append(f"No counters found for {pick}.")

        # Filtrar brawlers eliminando los baneados
        available_brawlers = {name: b for name, b in brawlers.items() if name not in banned_brawlers}
        # Añadir información de los brawlers disponibles
        selection_word = "selection" if phase in [1, 4] else "selections"
        summary.append(f"\nAvailable Brawlers (Your {selection_word} must be from this list, with their tier in parentheses):")
        summary.append(", ".join([f"{brawler.name} ({brawler.tier})" for brawler in available_brawlers.values()]))

    return "\n".join(summary)

def generate_final_prompt(phase, selected_map, maps, brawlers, banned_brawlers, team, picks, prompts_path="data/prompts", output_folder="final_prompt"):
    """
    Genera un archivo final combinando los prompts en el orden correcto:
    1. prompt_1.txt
    2. prompt_2.x.txt (según la fase)
    3. prompt_3.txt
    4. Información del mapa seleccionado
    5. Información de los brawlers disponibles (sin los baneados)

    Parámetros:
    - phase (int): Fase del draft (1 a 4).
    - selected_map (str): Nombre del mapa seleccionado.
    - maps (dict): Diccionario con los objetos Map.
    - brawlers (dict): Diccionario con los objetos Brawler.
    - banned_brawlers (list): Lista de brawlers baneados en esta partida.
    - prompts_folder (str): Carpeta donde están los prompts.
    - output_folder (str): Carpeta donde se guardará el archivo final.
    """

    # Definir las rutas de las carpetas
    current_directory = os.getcwd()
    final_path = os.path.join(current_directory, output_folder)

    # Crear la carpeta de salida si no existe
    os.makedirs(final_path, exist_ok=True)

    # Mapear el archivo de la fase correspondiente
    phase_prompts = {
        1: "prompt_2.1.txt",
        2: "prompt_2.23.txt",
        3: "prompt_2.45.txt",
        4: "prompt_2.6.txt"
    }

    # Obtener el nombre correcto del archivo de fase
    prompt_2_filename = phase_prompts.get(phase)

    if not prompt_2_filename:
        raise ValueError(f"Fase no válida: {phase}. Debe estar entre 1 y 4.")

    # Definir rutas de los archivos de los prompts
    prompt_1_path = os.path.join(prompts_path, "prompt_1.txt")
    prompt_2_path = os.path.join(prompts_path, prompt_2_filename)
    prompt_3_path = os.path.join(prompts_path, "prompt_3.txt")
    final_prompt_path = os.path.join(final_path, "final_prompt.txt")

    # Función para leer archivos de texto
    def read_file(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    # Leer los archivos en orden correcto
    final_content = (
        read_file(prompt_1_path) + "\n\n" +
        read_file(prompt_2_path) + "\n\n" +
        read_file(prompt_3_path) + "\n\n"
    )

    # Agregar la información del draft usando la función get_draft_summary()
    draft_summary_text = get_draft_summary(phase, team, banned_brawlers, picks, brawlers)

    # Añadir el resumen del draft al archivo final
    final_content += draft_summary_text + "\n\n"

    # Añadir información del mapa seleccionado
    if selected_map in maps:
        final_content += "Selected Map Information\n"
        final_content += str(maps[selected_map]) + "\n\n"
    else:
        raise ValueError(f"The selected map '{selected_map}' is not found in the 'maps' dictionary.")

    # Guardar el archivo final
    with open(final_prompt_path, "w", encoding="utf-8") as final_file:
        final_file.write(final_content)

    print(f"Final prompt file created at: {final_prompt_path}")

    return final_content
