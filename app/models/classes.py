# Clase Brawler con la nueva funcionalidad de imprimir todas las características
"""
Este módulo define las clases Brawler y Map para modelar estrategias en Brawl Stars.
"""
class Brawler:
    """Clase que representa un brawler y sus características, como counters y tier."""
    def __init__(self, name):
        self.name = name
        self.counters = []  # Vector que contendrá los brawlers que counterea
        self.tier = None    # Tier del brawler: S, A, B, C, D

    def add_counter(self, brawler):
        """Agrega un brawler a la lista de counters de este brawler."""
        self.counters.append(brawler)

    def __str__(self):
        """Devuelve una representación en cadena del brawler."""
        # Unir los nombres de los counters con una coma y espacio
        return (
            f"Brawler: {self.name}\n"
            f"  - Countered by: {', '.join([counter.name for counter in self.counters])}\n"
            f"  - Tier: {self.tier}\n"
        )



# Definimos la clase Mapa
class Map:
    """ 
    Clase que representa un mapa del juego con información sobre picks recomendados y estrategias.
    """
    def __init__(self, name, mode, has_indestructible_walls=False,
             first_pick=None, last_pick=None, other_picks=None, mid=None, lane=None, strategy=None):
        self.name = name
        self.mode = mode
        self.has_indestructible_walls = has_indestructible_walls
        self.first_pick = first_pick if first_pick else []
        self.last_pick = last_pick if last_pick else []
        self.other_picks = other_picks if other_picks else []
        self.mid = mid
        self.lane = lane
        self.strategy = strategy

    def __str__(self):
        # Convertir las listas en cadenas separadas por comas
        first_pick_text = ", ".join([brawler.name for brawler in self.first_pick])
        last_pick_text = ", ".join([brawler.name for brawler in self.last_pick])
        other_picks_text = ", ".join([brawler.name for brawler in self.other_picks])

        # Cambiar la forma en que se muestra el valor de has_indestructible_walls
        walls_text = "Yes" if self.has_indestructible_walls else "No"

        # Crear la cadena para mostrar
        return (
            f"Map: {self.name}\n"
            f"  - Mode: {self.mode}\n"
            f"  - Has indestructible walls: {walls_text}\n"
            f"  - Recommended picks for phase 1: {first_pick_text}\n"
            f"  - Recommended picks for phases 2 and 3: {other_picks_text}\n"
            f"  - Recommended picks for phase 4: {last_pick_text}\n"
            #f"  - Mid: {self.mid}\n"
            #f"  - Lane: {self.lane}\n"
            f"  - Estrategy: {self.strategy}"
        )
