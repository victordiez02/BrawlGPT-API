"""Este módulo contiene todas las funciones."""
import os
import re
from termcolor import colored
from tabulate import tabulate
from app.models.classes import Brawler, Map

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
        print("Please enter the draft phase (1-4) based on your current stage:")
        print("1: First phase - Choose the 1st pick. This is the first pick of the draft.")
        print("2: Second phase - Choose the 2nd and 3rd picks. This is the second part of the draft.")
        print("3: Third phase - Choose the 4th and 5th picks. This is the third part of the draft.")
        print("4: Fourth phase - Choose the last pick. This is the final pick of the draft.")

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

def ban_phase(team, brawlers):
    """Fase de baneos donde dos equipos eligen 3 brawlers para banear."""
    # Crear una copia del diccionario de brawlers

    # Baneos del primer equipo

    def default_message(i, team):
        """Función que imprime el mensaje predeterminado con el color adecuado según el equipo"""
        if (not i and team == "blue") or (i and team == "red"):
            print("\nTeam " + colored('Blue', 'blue', attrs=['bold']) + ": choose 3 brawlers to ban (one by one):")
        else:
            print("\nTeam " + colored('Red', 'red', attrs=['bold']) + ": choose 3 brawlers to ban (one by one):")

    blue_bans = []
    for i in range(3):
        ban_completed = False
        while not ban_completed:
            default_message(0, team)
            print(f"\nBan {i + 1}:")
            #print("Brawlers disponibles para banear:")
            #for brawler in remaining_brawlers:
            #    print(f"- {brawler}")
            brawler_to_ban = input("Enter the name of the brawler to ban: ").strip()
            clean_console()
            if brawler_to_ban in brawlers:
                if brawler_to_ban not in blue_bans:
                    blue_bans.append(brawler_to_ban)
                    #remaining_brawlers.pop(brawler_to_ban)
                    ban_completed = True
                else:
                    print(f"The brawler '{brawler_to_ban}' has already been banned. Please choose another one.")
            else:
                print(f"The brawler '{brawler_to_ban}' does not exist. Please choose another one.")
            if blue_bans:  # Verifica si blue_bans no está vacío
                if team == "blue":
                    print("\nBanned brawlers by the " + colored('Blue', 'blue', attrs=['bold']) + " team:")
                else:
                    print("\nBanned brawlers by the " + colored('Red', 'red', attrs=['bold']) + " team:")
                print(", ".join(blue_bans))
    clean_console()

    # Baneos del segundo equipo
    red_bans = []
    for i in range(3):
        ban_completed = False
        while not ban_completed:
            default_message(1, team)
            print(f"\nBan {i + 1}:")
            #print("Brawlers disponibles para banear:")
            #for brawler in remaining_brawlers:
            #    print(f"- {brawler}")
            brawler_to_ban = input("Enter the name of the brawler to ban: ").strip()
            clean_console()
            if brawler_to_ban in brawlers:
                if brawler_to_ban not in red_bans:
                    red_bans.append(brawler_to_ban)
                    #if brawler_to_ban not in blue_bans:
                    #   remaining_brawlers.pop(brawler_to_ban)
                    ban_completed = True
                else:
                    print(f"The brawler '{brawler_to_ban}' has already been banned. Please choose another one.")
            else:
                print(f"The brawler '{brawler_to_ban}' does not exist. Please choose another one.")
            if red_bans:  # Verifica si red_bans no está vacío
                if team == "blue":
                    print("\nBanned brawlers by the " + colored('Red', 'red', attrs=['bold']) + " team:")
                else:
                    print("\nBanned brawlers by the " + colored('Blue', 'blue', attrs=['bold']) + " team:")
                print(", ".join(red_bans))
    clean_console()

    banned_brawlers = list(set(red_bans + blue_bans))

    return banned_brawlers

def first_pick_phase(team, banned_brawlers, brawlers):
    """Fase de first pick"""

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y el primer pick."""
        print(colored('Banned brawlers:', 'magenta', attrs=['bold']) + " " + ", ".join(banned_brawlers))
        print(colored('First pick:', 'green', attrs=['bold']))
        if team == "blue":
            print(f"\nTURN: {colored('BLUE', 'blue', attrs=['bold'])}")
        else:
            print(f"\nTURN: {colored('RED', 'red', attrs=['bold'])}")

    # First pick
    pick_completed = False
    while not pick_completed:
        default_message()
        picked_brawler = input("Enter the name of the brawler: ").strip()
        clean_console()
        if picked_brawler in banned_brawlers:
            print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
        else:
            if picked_brawler in brawlers:
                pick_completed = True
            else:
                print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return picked_brawler

def second_third_phase(team, banned_brawlers, first_pick, brawlers):
    """Fase de segundo y tercer pick"""

    second_third_pick = []

    def default_message(team, second_third_pick):
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""

        # Imprimir los baneos (se asume que banned_brawlers está definido previamente)
        print(colored('Banned brawlers:', 'magenta', attrs=['bold']) + " " + ", ".join(banned_brawlers))

        # Imprimir First pick con el equipo que lo eligió
        if team == "blue":
            print(colored('First pick: ', 'green', attrs=['bold']) + first_pick + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))
        elif team == "red":
            print(colored('First pick: ', 'green', attrs=['bold']) + first_pick + " " + colored("[Chosen by red]", 'red', attrs=['bold']))

        # Imprimir Second pick con el equipo que lo eligió
        if second_third_pick:
            if team == "blue":
                print(colored('Second pick: ', 'green', attrs=['bold']) + second_third_pick[0] + " " + colored("[Chosen by red]", 'red', attrs=['bold']))
            elif team == "red":
                print(colored('Second pick: ', 'green', attrs=['bold']) + second_third_pick[0] + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))

        if team == "blue":
            print(f"\nTURN: {colored('RED', 'red', attrs=['bold'])}")
        else:
            print(f"\nTURN: {colored('BLUE', 'blue', attrs=['bold'])}")

    # Segundo y tercer pick
    for i in range(2):
        pick_completed = False
        while not pick_completed:
            default_message(team, second_third_pick)
            print(colored("\nThird pick:" if i else "\nSecond pick:", 'green', attrs=['bold']))
            picked_brawler = input("Enter the name of the brawler: ").strip()
            clean_console()
            if picked_brawler in banned_brawlers:
                print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
            else:
                if picked_brawler in brawlers:
                    if picked_brawler == first_pick or picked_brawler in second_third_pick:
                        print(f"The brawler '{picked_brawler}' has already been choosen. Please choose another one.")
                    else:
                        pick_completed = True
                        second_third_pick.append(picked_brawler)
                else:
                    print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return second_third_pick

def fourth_fifth_phase(team, banned_brawlers, first_pick, second_third_pick, brawlers):
    """Fase de cuarto y quinto pick"""

    fourth_fifth_pick = []

    def default_message(team, second_third_pick, fourth_fifth_pick):
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""

        # Imprimir baneos (se asume que banned_brawlers ya está definido)
        print(colored('Banned brawlers:', 'magenta', attrs=['bold']) + " " + ", ".join(banned_brawlers))

        # Imprimir First pick con el equipo que lo eligió
        if team == "blue":
            print(colored('First pick: ', 'green', attrs=['bold']) + first_pick + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))
        elif team == "red":
            print(colored('First pick: ', 'green', attrs=['bold']) + first_pick + " " + colored("[Chosen by red]", 'red', attrs=['bold']))

        # Imprimir Second and third pick con el equipo que lo eligió
        if second_third_pick:
            if team == "blue":
                print(colored('Second pick: ', 'green', attrs=['bold']) + second_third_pick[0] + " " + colored("[Chosen by red]", 'red', attrs=['bold']))
                print(colored('Third pick: ', 'green', attrs=['bold']) + second_third_pick[1] + " " + colored("[Chosen by red]", 'red', attrs=['bold']))
            elif team == "red":
                print(colored('Second pick: ', 'green', attrs=['bold']) + second_third_pick[0] + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))
                print(colored('Third pick: ', 'green', attrs=['bold']) + second_third_pick[1] + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))

        # Imprimir Fourth and Fifth pick con el equipo que lo eligió
        if fourth_fifth_pick:
            if team == "blue":
                print(colored('Fourth pick: ', 'green', attrs=['bold']) + fourth_fifth_pick[0] + " " + colored("[Chosen by blue]", 'blue', attrs=['bold']))
            elif team == "red":
                print(colored('Fourth pick: ', 'green', attrs=['bold']) + fourth_fifth_pick[0] + " " + colored("[Chosen by red]", 'red', attrs=['bold']))

        if team == "blue":
            print(f"\nTURN: {colored('BLUE', 'blue', attrs=['bold'])}")
        else:
            print(f"\nTURN: {colored('RED', 'red', attrs=['bold'])}")

    # Cuarto y quinto pick
    for i in range(2):
        pick_completed = False
        while not pick_completed:
            default_message(team, second_third_pick, fourth_fifth_pick)
            print(colored("\nFifth pick:" if i else "\nFourth pick:", 'green', attrs=['bold']))
            picked_brawler = input("Enter the name of the brawler: ").strip()
            clean_console()
            if picked_brawler in banned_brawlers:
                print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
            else:
                if picked_brawler in brawlers:
                    if picked_brawler == first_pick or picked_brawler in second_third_pick or picked_brawler in fourth_fifth_pick:
                        print(f"The brawler '{picked_brawler}' has already been choosen. Please choose another one.")
                    else:
                        pick_completed = True
                        fourth_fifth_pick.append(picked_brawler)
                else:
                    print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return fourth_fifth_pick

def last_phase(banned_brawlers, first_pick, second_third_pick, fourth_fifth_pick, brawlers):
    """Fase de last pick"""

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""
        print(colored('Banned brawlers:', 'magenta', attrs=['bold']) + " " + ", ".join(banned_brawlers))
        print(colored('First pick: ', 'green', attrs=['bold']) + first_pick)
        print(colored('Second and third pick: ', 'green', attrs=['bold']) + " " + ", ".join(second_third_pick))
        print(colored('Fourth and fifth pick: ', 'green', attrs=['bold']) + " " + ", ".join(fourth_fifth_pick))
        print(colored("\nLast pick:", 'green', attrs=['bold']))

    # Last pick
    pick_completed = False
    while not pick_completed:
        default_message()
        picked_brawler = input("Enter the name of the brawler: ").strip()
        clean_console()
        if picked_brawler in banned_brawlers:
            print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
        else:
            if picked_brawler in brawlers:
                if picked_brawler == first_pick or picked_brawler in second_third_pick or picked_brawler in fourth_fifth_pick:
                    print(f"The brawler '{picked_brawler}' has already been choosen. Please choose another one.")
                else:
                    pick_completed = True
            else:
                print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return picked_brawler

def draft(phase, team, brawlers):
    """Función que realiza el drafteo hasta la fase indicada"""
    banned_brawlers = ban_phase(team, brawlers)

    picks_list = []

    if phase >= 2:
        first_pick = first_pick_phase(team, banned_brawlers, brawlers)  # Siempre se pide el first pick
        picks_list.append(first_pick)

    if phase >= 3:
        second_third_pick = second_third_phase(team, banned_brawlers, first_pick, brawlers)  # Se pide second y third pick si estamos en fase 2 o superior
        picks_list.append(second_third_pick[0])  # 2nd pick
        picks_list.append(second_third_pick[1])  # 3rd pick

    if phase == 4:
        fourth_fifth_pick = fourth_fifth_phase(team, banned_brawlers, first_pick, second_third_pick, brawlers)  # Se pide fourth y fifth pick si estamos en fase 3 o superior
        picks_list.append(fourth_fifth_pick[0])  # 4th pick
        picks_list.append(fourth_fifth_pick[1])  # 5th pick

    return banned_brawlers, picks_list

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

def print_draft_summary(selected_map, phase, team, banned_brawlers, picks):
    """Función que imprime el resumen del draft en dos columnas con los picks correspondientes."""

    # Imprimir el título "CURRENT DRAFT" en negrita y color
    print(colored("CURRENT DRAFT", 'cyan', attrs=['bold']))

    # Imprimir el nombre del mapa en negrita y color
    print(colored(f"Selected Map: {selected_map}", 'green', attrs=['bold']))

    # Imprimir la fase en que se encuentra el draft
    print(colored(f"Phase {phase}", 'yellow', attrs=['bold']))

    # Determinar el equipo que elige en este turno y aplicar color
    if phase % 2:  # Fase impar → elige el equipo que comenzó
        next_turn = "BLUE" if team == "blue" else "RED"
    else:  # Fase par → elige el equipo contrario
        next_turn = "RED" if team == "blue" else "BLUE"

    turn_color = 'blue' if next_turn == "BLUE" else 'red'
    print(colored(f"NEXT TURN: {next_turn}", turn_color, attrs=['bold']))

    # Imprimir los baneos en color magenta
    print(colored('\nBanned Brawlers:', 'magenta', attrs=['bold']) + " " + (", ".join(banned_brawlers) if banned_brawlers else "None"))

    # Determinar los picks de cada equipo basados en el equipo que comenzó
    if team == "blue":
        # El equipo azul ha elegido primero
        team_1_picks = [picks[0] if len(picks) > 0 else "---", picks[3] if len(picks) > 3 else "---", picks[4] if len(picks) > 4 else "---"]  # 1st, 4th, 5th picks
        team_2_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", picks[5] if len(picks) > 5 else "---"]  # 2nd, 3rd, 6th picks
        team_1_name = colored("Blue Team", 'blue', attrs=['bold'])
        team_2_name = colored("Red Team", 'red', attrs=['bold'])
    else:
        # El equipo rojo ha elegido primero
        # CORRECCIÓN: Mantener la lógica de asignación correcta
        team_1_picks = [picks[0] if len(picks) > 0 else "---", picks[3] if len(picks) > 3 else "---", picks[4] if len(picks) > 4 else "---"]  # 1st, 4th, 5th picks
        team_2_picks = [picks[1] if len(picks) > 1 else "---", picks[2] if len(picks) > 2 else "---", picks[5] if len(picks) > 5 else "---"]  # 2nd, 3rd, 6th picks
        team_1_name = colored("Red Team", 'red', attrs=['bold'])
        team_2_name = colored("Blue Team", 'blue', attrs=['bold'])

    # Construir la tabla con `tabulate`
    table_data = []
    for i in range(3):
        pick_1 = team_1_picks[i] if team_1_picks[i] != "---" else "---"
        pick_2 = team_2_picks[i] if team_2_picks[i] != "---" else "---"
        table_data.append([pick_1, pick_2])

    print("\n" + tabulate(table_data, headers=[team_1_name, team_2_name], tablefmt="fancy_grid"))

    print("\n")

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
        final_content += str(selected_map) + "\n\n"
    else:
        raise ValueError(f"The selected map '{selected_map}' is not found in the 'maps' dictionary.")

    # Guardar el archivo final
    with open(final_prompt_path, "w", encoding="utf-8") as final_file:
        final_file.write(final_content)

    print(f"Final prompt file created at: {final_prompt_path}")

    return final_content

def parse_gemini_response(response_text):
    """
    Convierte la respuesta de Gemini en un JSON estructurado.
    Devuelve una lista de objetos con 'brawlers' y 'probability'.
    """
    suggestions = []
    lines = response_text.strip().split("\n")

    for line in lines:
        match = re.match(r"\d+\.\s(.*?)\s-\s(\d+)%", line)
        if match:
            brawlers = match.group(1).split(" + ")  # Separar los brawlers
            probability = int(match.group(2))  # Extraer el porcentaje
            suggestions.append({"brawlers": brawlers, "probability": probability})

    return {"gemini_suggestions": suggestions}
