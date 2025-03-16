"""
Módulo encargado de gestionar la interacción con la API de Gemini.

Funciones:
- call_gemini(prompt): Envía un prompt a la API de Gemini y obtiene la respuesta.
- parse_gemini_response(response_text): Procesa la respuesta de Gemini y la estructura en JSON.
"""
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.draft_service import print_json

# Cargar variables de entorno
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini(prompt):
    """
    Envía un prompt a la API de Gemini y devuelve la respuesta estructurada.

    Parámetros:
    - prompt (str): Texto con la información del draft.

    Retorna:
    - dict: Lista de brawlers sugeridos con sus probabilidades.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    # Parsea la respuesta generada por Gemini en un json.
    parse_response = parse_gemini_response(response.text)

    # Imprime la respuesta generada por Gemini en la consola.
    print_json(parse_response)

    return parse_response if response.text else "No response from Gemini."

import re

def parse_gemini_response(response_text):
    """
    Convierte la respuesta de Gemini en un JSON estructurado.

    Parámetros:
    - response_text (str): Texto devuelto por la API.

    Retorna:
    - dict: Lista de sugerencias con brawlers, probabilidades y explicaciones.
    """
    suggestions = []
    lines = response_text.strip().split("\n")

    # Procesamos las líneas de la respuesta
    for line in lines:
        # Regular expression para capturar el brawler, porcentaje, explicación en inglés y explicación en español
        # Este formato es el que ahora esperamos:
        # "[Brawler Name] | [Percentage]% | [Explanation in English] | [Explanation in Spanish]"
        
        match = re.match(r"(\d+\.)?\s*(.*?)\s*\|\s*(\d+)%\s*\|\s*(.*?)\s*\|\s*(.*)", line)

        if match:
            brawlers = match.group(2).strip()  # Nombre del brawler
            # Eliminar asteriscos del nombre de los brawlers
            brawlers = brawlers.replace("**", "").strip()

            probability = int(match.group(3))  # Probabilidad
            explanationUSA = match.group(4).strip()  # Explicación en inglés
            explanationESP = match.group(5).strip()  # Explicación en español

            # Eliminar cualquier carácter extra que pueda haberse incluido (como asteriscos)
            explanationUSA = explanationUSA.replace("**", "").strip()
            explanationESP = explanationESP.replace("**", "").strip()

            # Manejo del caso en el que el brawler y la probabilidad se repiten antes de la explicación en español
            duplicate_pattern = rf"^\s*{re.escape(brawlers)}\s*\|\s*{probability}%\s*\|"
            explanationESP = re.sub(duplicate_pattern, "", explanationESP).strip()

            # Añadir la sugerencia al listado
            suggestions.append({
                "brawlers": brawlers,
                "probability": probability,
                "explanationUSA": explanationUSA,
                "explanationESP": explanationESP
            })

    return {"gemini_suggestions": suggestions}
