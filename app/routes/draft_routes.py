"""
Módulo encargado de definir las rutas de la API en FastAPI.

Rutas:
- `POST /draft`: Maneja el draft, generando un resumen del proceso y obteniendo recomendaciones de Gemini.

Funciones:
- handle_draft(request: Request, draft_request: DraftRequest):
    - Procesa la solicitud del draft, generando el resumen y el prompt para la IA.
    - Llama a `execute_draft()` para manejar la lógica del draft.
    - Envía el prompt a `call_gemini()` para obtener recomendaciones de brawlers.
    - Devuelve un JSON con el resumen del draft y la recomendación de Gemini.

Dependencias:
- FastAPI para la gestión de rutas.
- `DraftRequest` de `app.models.draft_model` para validar la estructura de la solicitud.
- `execute_draft` de `app.services.draft_service` para manejar la lógica del draft.
- `call_gemini` de `app.services.gemini_service` para obtener recomendaciones de IA.

Notas:
- `maps` y `brawlers` no se cargan aquí, sino en `main.py` y se acceden desde `request.app.state`.
- Maneja excepciones como `ValueError`, `FileNotFoundError` y `KeyError`, devolviendo respuestas HTTP adecuadas.
"""
import os
from fastapi import APIRouter, HTTPException, Request, Header
from app.models.draft_model import DraftRequest
from app.services.draft_service import execute_draft
from app.services.gemini_service import call_gemini

router = APIRouter()

@router.post("/draft")
def handle_draft(request: Request, draft_request: DraftRequest, x_api_key: str = Header(None)):
    """
    Maneja el draft, genera el resumen y obtiene sugerencias de Gemini.

    Parámetros:
    - request (Request): Petición de FastAPI para acceder a `maps` y `brawlers`.
    - draft_request (DraftRequest): Datos enviados en la petición.

    Retorna:
    - dict: JSON con el resumen del draft y la recomendación de Gemini.
    """

    if x_api_key != os.getenv("BRAWLGPT_API_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")

    try:
        # Obtener `maps` y `brawlers` desde la aplicación
        maps = request.app.state.maps
        brawlers = request.app.state.brawlers

        # Ejecutar la lógica del draft
        draft_data = execute_draft(
            draft_request.phase,
            draft_request.selected_map,
            maps,
            brawlers,
            draft_request.banned_brawlers,
            draft_request.team,
            draft_request.picks
        )

        # Obtener respuesta de Gemini
        gemini_response = call_gemini(draft_data["prompt"])

        # Devolver el resultado en formato JSON
        return {
            "gemini_response": gemini_response
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value error: {str(e)}") from e

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}") from e

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Key error: {str(e)}") from e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e
