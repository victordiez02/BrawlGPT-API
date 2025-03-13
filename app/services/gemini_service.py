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
    - dict: Lista de sugerencias con brawlers, probabilidades y explicaciones.
    """
    suggestions = []
    lines = response_text.strip().split("\n")

    # Procesamos las líneas de la respuesta
    for line in lines:
        # Regular expression to extract brawlers, probability, explanation (in both English and Spanish)
        # Esto debería capturar el formato de la respuesta: 
        # "[Brawler Name] - [Percentage]% - [Explanation] - [Translation]"
        # o bien: "[Brawler Name 1] + [Brawler Name 2] - [Percentage]% - [Explanation] - [Translation]"
        
        match = re.match(r"(\d+\.)?\s*(.*?)\s*-\s*(\d+)%\s*-\s*(.*?)\s*-\s*\*(.*?)\*", line)
        
        if match:
            brawlers = match.group(2).strip()  # Nombre del brawler o pareja de brawlers
            probability = int(match.group(3))  # Probabilidad
            explanationUSA = match.group(4).strip()  # Explicación en inglés
            explanationESP = match.group(5).strip()  # Explicación en español

            # Eliminar caracteres de negrita '**' en la explicación en inglés y español
            brawlers = brawlers.replace("**", "").strip()
            explanationUSA = explanationUSA.replace("**", "").strip()
            explanationESP = explanationESP.replace("**", "").strip()

            # Añadir la sugerencia al listado
            suggestions.append({
                "brawlers": brawlers,
                "probability": probability,
                "explanationUSA": explanationUSA,
                "explanationESP": explanationESP
            })

    return {"gemini_suggestions": suggestions}
