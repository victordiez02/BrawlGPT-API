"""
Módulo encargado de gestionar la lógica del sistema de draft en Brawl Stars.

Funciones:
- ban_phase(team, brawlers): Maneja la fase de baneos de los brawlers.
- first_pick_phase(team, banned_brawlers, brawlers): Gestiona la selección del primer pick.
- second_third_phase(team, banned_brawlers, first_pick, brawlers): Maneja la selección del segundo y tercer pick.
- fourth_fifth_phase(team, banned_brawlers, first_pick, second_third_pick, brawlers): Maneja la selección del cuarto y quinto pick.
- last_phase(banned_brawlers, first_pick, second_third_pick, fourth_fifth_pick, brawlers): Maneja la selección del último pick.
- draft(phase, team, brawlers): Ejecuta el draft hasta la fase indicada.
- print_draft_summary(selected_map, phase, team, banned_brawlers, picks): Imprime el resumen del draft en formato tabular.
- execute_draft(phase, selected_map, maps, brawlers, banned_brawlers, team, picks): Ejecuta el proceso del draft, genera el resumen y el prompt para la IA.
"""

from tabulate import tabulate
from termcolor import colored
from app.utils.config import clean_console, get_draft_summary, generate_final_prompt

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

def execute_draft(phase, selected_map, maps, brawlers, banned_brawlers, team, picks):
    """
    Ejecuta el proceso del draft y genera los datos necesarios.

    Parámetros:
    - phase (int): Número de la fase actual del draft.
    - selected_map (str): Nombre del mapa seleccionado.
    - maps (dict): Diccionario con los datos de los mapas.
    - brawlers (dict): Diccionario con los datos de los brawlers.
    - banned_brawlers (list): Lista de brawlers que han sido baneados.
    - team (str): Equipo que está eligiendo en esta fase.
    - picks (list): Lista de brawlers seleccionados hasta el momento.

    Retorna:
    - dict: Un diccionario con:
        - "draft_summary": Resumen del draft en texto.
        - "prompt": Prompt generado para la IA.
    """
    # Generar el resumen del draft
    draft_summary = get_draft_summary(phase, team, banned_brawlers, picks, brawlers)

    # Generar el prompt para la IA
    prompt = generate_final_prompt(
        phase, selected_map, maps, brawlers, banned_brawlers, team, picks
    )

    # Imprimir el resumen en consola
    print_draft_summary(selected_map, phase, team, banned_brawlers, picks)
    print("\nVersión 1.0.1")

    return {
        "draft_summary": draft_summary,
        "prompt": prompt
    }
