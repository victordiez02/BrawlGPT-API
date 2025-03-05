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

    print(response.text)

    return parse_gemini_response(response.text) if response.text else "No response from Gemini."


def parse_gemini_response(response_text):
    """
    Convierte la respuesta de Gemini en un JSON estructurado.

    Parámetros:
    - response_text (str): Texto devuelto por la API.

    Retorna:
    - dict: Lista de sugerencias con brawlers y probabilidades.
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
