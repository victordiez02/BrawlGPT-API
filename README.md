# 📈 BrawlGPT Draft API

Este proyecto es una API en **FastAPI** que gestiona un **sistema de draft** para Brawl Stars.
Incluye la lógica de selección y baneo de brawlers, integración con **Gemini AI** para recomendaciones y un sistema modular bien estructurado.

---

## 📁 **Estructura del Proyecto**
El código está distribuido en varios módulos para facilitar la **organización** y **mantenimiento**.

📀 **Estructura principal:**
```
📁 app/
 ┗📁 models/         # 📌 Modelos de datos
   ┗ draft_model.py   # ✅ `DraftRequest` (estructura de la API)
 ┗📁 routes/         # 📌 Rutas de la API
   ┗ draft_routes.py  # ✅ Endpoint `/draft`
 ┗📁 services/       # 📌 Lógica del draft y conexión con Gemini
   ┗ draft_service.py # ✅ Lógica del draft (bans, picks, resumen)
   ┗ gemini_service.py # ✅ Comunicación con Gemini AI
 ┗📁 utils/          # 📌 Funciones auxiliares y configuración
   ┗ config.py        # ✅ Carga de datos, consola y prompts
 ┗ main.py            # ✅ Punto de entrada de FastAPI
```

---

## 🔹 **Ubicación de cada función**

### 📌 **1. `app/models/draft_model.py`**
👉 Define la estructura de los datos que recibe la API.

| 📀 Función | 📀 Descripción |
|-----------|--------------|
| `DraftRequest` | Modelo de datos que valida la petición a `/draft`. |

### 📌 **2. `app/routes/draft_routes.py`**
👉 Contiene las rutas de la API (FastAPI).

| 📀 Función | 📀 Descripción |
|-----------|--------------|
| `handle_draft(request: DraftRequest)` | Procesa el draft y obtiene sugerencias de Gemini. |

### 📌 **3. `app/services/draft_service.py`**
👉 Contiene toda la **lógica del draft**.

| 📀 Función | 📀 Descripción |
|-----------|--------------|
| `ban_phase()` | Maneja la fase de baneos. |
| `first_pick_phase()` | Selección del primer pick. |
| `second_third_phase()` | Selección del segundo y tercer pick. |
| `fourth_fifth_phase()` | Selección del cuarto y quinto pick. |
| `last_phase()` | Última selección. |
| `draft()` | Ejecuta el draft hasta la fase indicada. |
| `get_draft_summary()` | Genera un resumen del draft para la IA. |
| `print_draft_summary()` | Imprime el resumen del draft. |
| `execute_draft()` | Genera el resumen del draft y el prompt. |

### 📌 **4. `app/services/gemini_service.py`**
👉 Maneja la conexión con la **API de Gemini**.

| 📀 Función | 📀 Descripción |
|-----------|--------------|
| `call_gemini()` | Envía el prompt a la API de Gemini y obtiene recomendaciones. |
| `parse_gemini_response()` | Convierte la respuesta de Gemini a un JSON estructurado. |

### 📌 **5. `app/utils/config.py`**
👉 Contiene **funciones auxiliares** y **carga de datos**.

| 📀 Función | 📀 Descripción |
|-----------|--------------|
| `clean_console()` | Limpia la consola. |
| `load_data()` | Carga la información de los brawlers. |
| `load_maps()` | Carga los mapas y sus características. |
| `get_team()` | Obtiene el equipo inicial. |
| `get_map()` | Obtiene el mapa seleccionado. |
| `get_phase()` | Obtiene la fase actual. |
| `generate_final_prompt()` | Genera el prompt para la IA. |

### 📌 **6. `main.py`**
👉 Punto de entrada de la API.
- Carga los datos de `brawlers` y `maps`.
- Almacena los datos en `app.state` para usarlos en todas las rutas.
- Registra las rutas con `app.include_router(draft_router)`.

---

## 💡 **Ejemplo de Petición a la API**
👉 **Enviando datos al endpoint `/draft`**
```json
{
  "phase": 2,
  "selected_map": "Hard Rock Mine",
  "banned_brawlers": ["Spike", "Crow", "Rico"],
  "team": "blue",
  "picks": ["Brock"]
}
```

👉 **Respuesta esperada**
```json
{
  "draft_summary": "Resumen detallado del draft...",
  "gemini_response": {
    "gemini_suggestions": [
        {
            "brawlers": ["Maisie", "Stu"],
            "probability": 75
        },
        {
            "brawlers": ["Maisie", "Rico"],
            "probability": 70
        }
    ]
  }
}
```

---

## 🚀 **Conclusión**
🔹 Código **modular** y **bien estructurado**.  
🔹 Fácil de **buscar funciones** gracias a este README.  
🔹 **Listo para producción** con FastAPI y Gemini AI.  

🚀 **¡Ahora puedes trabajar con tu API de forma organizada y eficiente!** 🎯

## Notas Adicionales

**Para abrir enviroment:**  

brawlGPT-env\Scripts\activate.bat

**Para abrir servidor local:**  

uvicorn main:app --reload

**TEMPORADA 35**

El meta se ha sacado de este video de SpenLC:  
<https://www.youtube.com/watch?v=_aYrn_D-IQU>

Los tiers se han sacado de esta publicación de AshBS:  
<https://www.instagram.com/p/DFiXsv2RceZ/>

La información de mejores picks por mapa se han sacado de este video:  
<https://www.youtube.com/watch?v=S-8mUu3cnWI>

La información de como draftear se ha sacado de este video:  
<https://www.youtube.com/watch?v=YzfE6-v_5a8>
