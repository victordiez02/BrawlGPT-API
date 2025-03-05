"""
Módulo que define los modelos de datos para la API.

Modelos:
- DraftRequest: Representa la solicitud de draft con los datos necesarios para procesarlo.
"""
from typing import List
from pydantic import BaseModel

class DraftRequest(BaseModel):
    """
    Modelo de datos para representar la solicitud del draft.

    Atributos:
    - phase (int): Número de la fase del draft (1 a 4).
    - selected_map (str): Nombre del mapa seleccionado.
    - banned_brawlers (List[str]): Lista de brawlers que han sido baneados.
    - team (str): Equipo que está eligiendo en esta fase ('blue' o 'red').
    - picks (List[str]): Lista de brawlers seleccionados hasta el momento.
    """
    phase: int
    selected_map: str
    banned_brawlers: List[str]
    team: str
    picks: List[str]
