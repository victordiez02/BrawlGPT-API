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
- print_json(gemini_response): Imprime la respuesta de Gemini de manera formateada y legible en la consola.
"""

from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text
from app.utils.config import clean_console


def ban_phase(team, brawlers):
    """Fase de baneos donde dos equipos eligen 3 brawlers para banear."""
    
    def default_message(i, team):
        """Función que imprime el mensaje predeterminado con el color adecuado según el equipo"""
        if (not i and team == "blue") or (i and team == "red"):
            print(Text("\nTeam Blue: choose 3 brawlers to ban (one by one):", style="bold blue"))
        else:
            print(Text("\nTeam Red: choose 3 brawlers to ban (one by one):", style="bold red"))
    
    blue_bans = []
    for i in range(3):
        ban_completed = False
        while not ban_completed:
            default_message(0, team)
            print(f"\nBan {i + 1}:")
            brawler_to_ban = input("Enter the name of the brawler to ban: ").strip()
            clean_console()
            if brawler_to_ban in brawlers:
                if brawler_to_ban not in blue_bans:
                    blue_bans.append(brawler_to_ban)
                    ban_completed = True
                else:
                    print(f"The brawler '{brawler_to_ban}' has already been banned. Please choose another one.")
            else:
                print(f"The brawler '{brawler_to_ban}' does not exist. Please choose another one.")
            if blue_bans:
                team_color = "bold blue" if team == "blue" else "bold red"
                print(Text("\nBanned brawlers by the " + ("Blue" if team == "blue" else "Red") + " team:", style=team_color))
                print(", ".join(blue_bans))
    clean_console()
    
    red_bans = []
    for i in range(3):
        ban_completed = False
        while not ban_completed:
            default_message(1, team)
            print(f"\nBan {i + 1}:")
            brawler_to_ban = input("Enter the name of the brawler to ban: ").strip()
            clean_console()
            if brawler_to_ban in brawlers:
                if brawler_to_ban not in red_bans:
                    red_bans.append(brawler_to_ban)
                    ban_completed = True
                else:
                    print(f"The brawler '{brawler_to_ban}' has already been banned. Please choose another one.")
            else:
                print(f"The brawler '{brawler_to_ban}' does not exist. Please choose another one.")
            if red_bans:
                team_color = "bold red" if team == "blue" else "bold blue"
                print(Text("\nBanned brawlers by the " + ("Red" if team == "blue" else "Blue") + " team:", style=team_color))
                print(", ".join(red_bans))
    clean_console()
    
    return list(set(red_bans + blue_bans))

def first_pick_phase(team, banned_brawlers, brawlers):
    """Fase de first pick"""

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y el primer pick."""
        print(Text("Banned brawlers: ", style="bold magenta") + ", ".join(banned_brawlers))
        print(Text("First pick:", style="bold green"))
        turn_text = Text("\nTURN: BLUE", style="bold blue") if team == "blue" else Text("\nTURN: RED", style="bold red")
        print(turn_text)

    pick_completed = False
    while not pick_completed:
        default_message()
        picked_brawler = input("Enter the name of the brawler: ").strip()
        clean_console()
        if picked_brawler in banned_brawlers:
            print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
        elif picked_brawler in brawlers:
            pick_completed = True
        else:
            print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return picked_brawler

def second_third_phase(team, banned_brawlers, first_pick, brawlers):
    """Fase de segundo y tercer pick"""

    second_third_pick = []

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""
        print(Text("Banned brawlers: ", style="bold magenta") + ", ".join(banned_brawlers))
        print(Text("First pick: ", style="bold green") + first_pick + (Text(" [Chosen by blue]", style="bold blue") if team == "blue" else Text(" [Chosen by red]", style="bold red")))
        if second_third_pick:
            print(Text("Second pick: ", style="bold green") + second_third_pick[0] + (Text(" [Chosen by red]", style="bold red") if team == "blue" else Text(" [Chosen by blue]", style="bold blue")))
        turn_text = Text("\nTURN: RED", style="bold red") if team == "blue" else Text("\nTURN: BLUE", style="bold blue")
        print(turn_text)

    for i in range(2):
        pick_completed = False
        while not pick_completed:
            default_message()
            pick_label = Text("\nThird pick:", style="bold green") if i else Text("\nSecond pick:", style="bold green")
            print(pick_label)
            picked_brawler = input("Enter the name of the brawler: ").strip()
            clean_console()
            if picked_brawler in banned_brawlers or picked_brawler == first_pick or picked_brawler in second_third_pick:
                print(f"The brawler '{picked_brawler}' has already been chosen. Please choose another one.")
            elif picked_brawler in brawlers:
                pick_completed = True
                second_third_pick.append(picked_brawler)
            else:
                print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return second_third_pick

def fourth_fifth_phase(team, banned_brawlers, first_pick, second_third_pick, brawlers):
    """Fase de cuarto y quinto pick"""

    fourth_fifth_pick = []

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""
        print(Text("Banned brawlers: ", style="bold magenta") + ", ".join(banned_brawlers))
        print(Text("First pick: ", style="bold green") + first_pick + (Text(" [Chosen by blue]", style="bold blue") if team == "blue" else Text(" [Chosen by red]", style="bold red")))
        for idx, pick in enumerate(second_third_pick):
            print(Text(f"{['Second', 'Third'][idx]} pick: ", style="bold green") + pick + (Text(" [Chosen by red]", style="bold red") if team == "blue" else Text(" [Chosen by blue]", style="bold blue")))
        turn_text = Text("\nTURN: BLUE", style="bold blue") if team == "blue" else Text("\nTURN: RED", style="bold red")
        print(turn_text)

    for i in range(2):
        pick_completed = False
        while not pick_completed:
            default_message()
            pick_label = Text("\nFifth pick:", style="bold green") if i else Text("\nFourth pick:", style="bold green")
            print(pick_label)
            picked_brawler = input("Enter the name of the brawler: ").strip()
            clean_console()
            if picked_brawler in banned_brawlers or picked_brawler == first_pick or picked_brawler in second_third_pick or picked_brawler in fourth_fifth_pick:
                print(f"The brawler '{picked_brawler}' has already been chosen. Please choose another one.")
            elif picked_brawler in brawlers:
                pick_completed = True
                fourth_fifth_pick.append(picked_brawler)
            else:
                print(f"The brawler '{picked_brawler}' does not exist. Please choose another one.")
    clean_console()

    return fourth_fifth_pick

# Esta función no tiene sentido, ya que no se puede elegir el último pick.
def last_phase(banned_brawlers, first_pick, second_third_pick, fourth_fifth_pick, brawlers):
    """Fase de last pick"""

    def default_message():
        """Imprime el mensaje predeterminado con los brawlers baneados y los picks."""
        print(Text("Banned brawlers: ", style="bold magenta") + ", ".join(banned_brawlers))
        print(Text("First pick: ", style="bold green") + first_pick)
        print(Text("Second and third pick: ", style="bold green") + ", ".join(second_third_pick))
        print(Text("Fourth and fifth pick: ", style="bold green") + ", ".join(fourth_fifth_pick))
        print(Text("\nLast pick:", style="bold green"))

    pick_completed = False
    while not pick_completed:
        default_message()
        picked_brawler = input("Enter the name of the brawler: ").strip()
        clean_console()
        if picked_brawler in banned_brawlers:
            print(f"The brawler '{picked_brawler}' has already been banned. Please choose another one.")
        elif picked_brawler in brawlers:
            if picked_brawler == first_pick or picked_brawler in second_third_pick or picked_brawler in fourth_fifth_pick:
                print(f"The brawler '{picked_brawler}' has already been chosen. Please choose another one.")
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
    """ 
    Función que imprime el resumen del draft de forma clara y con formato estilizado usando `rich`. 
    """

    console = Console()

    # Encabezado principal con colores
    console.print(Text("CURRENT DRAFT", style="bold cyan"))
    console.print(Text(f"Selected Map: {selected_map}", style="bold green"))
    console.print(Text(f"Phase {phase}", style="bold yellow"))

    # Determinar el equipo que tiene el siguiente turno
    next_turn = "BLUE" if (phase % 2 and team == "blue") or (phase % 2 == 0 and team == "red") else "RED"
    turn_color = "bold blue" if next_turn == "BLUE" else "bold red"
    console.print(Text(f"NEXT TURN: {next_turn}", style=turn_color))

    # Mostrar brawlers baneados
    banned_text = ", ".join(banned_brawlers) if banned_brawlers else "None"
    console.print(Text("\nBanned Brawlers:", style="bold magenta"), banned_text)

    # Crear la tabla para mostrar los picks
    table = Table(title="Draft Picks", show_lines=True)

    # Determinar colores de equipo
    blue_team_name = Text("Blue Team", style="bold blue")
    red_team_name = Text("Red Team", style="bold red")

    table.add_column(blue_team_name, justify="center")
    table.add_column(red_team_name, justify="center")

    # Formatear los picks en la tabla
    team_1_picks = ["---"] * 3
    team_2_picks = ["---"] * 3

    if team == "blue":
        # El equipo azul ha elegido primero
        if len(picks) > 0: team_1_picks[0] = picks[0]  # 1st pick
        if len(picks) > 1: team_2_picks[0] = picks[1]  # 2nd pick
        if len(picks) > 2: team_2_picks[1] = picks[2]  # 3rd pick
        if len(picks) > 3: team_1_picks[1] = picks[3]  # 4th pick
        if len(picks) > 4: team_1_picks[2] = picks[4]  # 5th pick
        if len(picks) > 5: team_2_picks[2] = picks[5]  # 6th pick
    else:
        # El equipo rojo ha elegido primero
        if len(picks) > 0: team_2_picks[0] = picks[0]  # 1st pick
        if len(picks) > 1: team_1_picks[0] = picks[1]  # 2nd pick
        if len(picks) > 2: team_1_picks[1] = picks[2]  # 3rd pick
        if len(picks) > 3: team_2_picks[1] = picks[3]  # 4th pick
        if len(picks) > 4: team_2_picks[2] = picks[4]  # 5th pick
        if len(picks) > 5: team_1_picks[2] = picks[5]  # 6th pick

    # Agregar filas a la tabla
    for i in range(3):
        table.add_row(team_1_picks[i], team_2_picks[i])

    console.print(table)


def print_json(gemini_response):
    """
    Imprime la respuesta de Gemini de manera bonita y legible.

    Parámetros:
    - gemini_response (dict): JSON con las sugerencias de brawlers y sus detalles.
    
    Retorna:
    - None (Solo imprime en la consola).
    """
    console = Console()

    if "gemini_suggestions" not in gemini_response:
        console.print("[bold red]No valid suggestions found.[/bold red]")
        return

    table = Table(title="Best Brawler Options", show_lines=True)

    table.add_column("Brawlers", style="cyan", justify="center")
    table.add_column("Probability (%)", style="green", justify="center")
    table.add_column("Explanation (ENG)", style="yellow", justify="left", max_width=50)
    table.add_column("Explanation (ESP)", style="magenta", justify="left", max_width=50)

    for suggestion in gemini_response["gemini_suggestions"]:
        table.add_row(
            suggestion["brawlers"],
            str(suggestion["probability"]),
            suggestion["explanationUSA"],
            suggestion["explanationESP"]
        )

    console.print(table)
