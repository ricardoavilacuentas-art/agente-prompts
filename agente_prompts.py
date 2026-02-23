import anthropic

# ————————————————————————————————————————————————
# MANUALES DE MEJORES PRÁCTICAS POR IA
# ————————————————————————————————————————————————

MANUAL_CHATGPT = """
MEJORES PRÁCTICAS PARA PROMPTS DE CHATGPT/GPT-4:
- Asigna un rol específico: "Actúa como un experto en..."
- Sé específico con el formato de salida: "Responde en formato lista / tabla / párrafos"
- Usa ejemplos concretos para guiar la respuesta (few-shot prompting)
- Especifica el tono: formal, casual, técnico, creativo
- Indica la longitud esperada: "en menos de 100 palabras" o "de forma detallada"
- Divide tareas complejas en pasos: "Primero haz X, luego Y"
- Pide razonamiento paso a paso para problemas complejos: "Piensa paso a paso"
- Especifica restricciones: "Sin usar tecnicismos" o "Solo información verificada"
- Usa delimitadores para separar contexto: usa comillas o corchetes para datos de entrada
- Pide revisión al final: "Al terminar, revisa si cumpliste todos los requisitos"
"""

MANUAL_MIDJOURNEY = """
MEJORES PRÁCTICAS PARA PROMPTS DE MIDJOURNEY:
- Estructura: [sujeto principal], [descripción detallada], [entorno/fondo], [estilo artístico], [iluminación], [cámara/lente], [calidad]
- Usa modificadores de calidad: ultra detailed, highly detailed, 8k, photorealistic
- Especifica el estilo artístico: oil painting, watercolor, digital art, concept art, photography
- Define la iluminación: golden hour, studio lighting, cinematic lighting, soft light, dramatic shadows
- Agrega referencia de artista si aplica: "in the style of..."
- Usa parámetros al final: --ar 16:9 (proporción), --v 6 (versión), --q 2 (calidad)
- Sé muy descriptivo con colores: vivid colors, muted tones, monochromatic, pastel palette
- Incluye perspectiva/ángulo: bird's eye view, close-up, wide angle, portrait
- Evita palabras negativas — usa --no [elemento] para excluir cosas
- Los prompts en inglés funcionan mejor
"""

MANUAL_STABLE_DIFFUSION = """
MEJORES PRÁCTICAS PARA PROMPTS DE STABLE DIFFUSION:
- Estructura: [sujeto], [detalles del sujeto], [acción], [entorno], [estilo], [calidad técnica]
- Usa palabras clave de calidad: masterpiece, best quality, ultra-detailed, sharp focus, high resolution
- Especifica el modelo de arte: realistic, anime, illustration, concept art, 3D render
- Define la composición: centered, rule of thirds, symmetrical, dynamic pose
- Agrega términos técnicos de fotografía: DSLR, 85mm lens, depth of field, bokeh
- Usa prompts negativos para evitar problemas comunes: (deformed, bad anatomy, extra limbs, blurry:1.4)
- Pondera palabras importantes con paréntesis: (beautiful eyes:1.3) aumenta su importancia
- Especifica la iluminación: volumetric lighting, rim light, backlight, natural light
- Incluye el artista de referencia si aplica: "by greg rutkowski, artstation"
- Separa conceptos con comas y usa paréntesis para agrupar ideas relacionadas
"""

MANUAL_GEMINI = """
MEJORES PRÁCTICAS PARA PROMPTS DE GOOGLE GEMINI:
- Aprovecha su capacidad multimodal: puedes describir imágenes y texto juntos
- Sé conversacional y natural — Gemini responde bien al lenguaje cotidiano
- Proporciona contexto amplio: mientras más contexto, mejor la respuesta
- Pide comparaciones y análisis: Gemini es muy bueno evaluando múltiples perspectivas
- Usa instrucciones de formato explícitas: "Organiza tu respuesta con subtítulos"
- Para tareas creativas, describe el estado de ánimo o atmósfera deseada
- Aprovecha su conocimiento actualizado para preguntas sobre eventos recientes
- Pide fuentes o referencias cuando necesites información verificable
- Para código, especifica el lenguaje y el entorno de ejecución
- Combina instrucciones de rol + tarea + formato para mejores resultados
"""

# ————————————————————————————————————————————————
# SECCIÓN 1: LAS HERRAMIENTAS
# ————————————————————————————————————————————————

def crear_prompt_texto(objetivo, tono, contexto, ia_destino="ChatGPT"):
    manual = MANUAL_CHATGPT if "gpt" in ia_destino.lower() or "chat" in ia_destino.lower() else MANUAL_GEMINI
    prompt = f"""Usando estas mejores prácticas:
{manual}

Crea un prompt optimizado para {ia_destino} con estas características:
- Objetivo: {objetivo}
- Tono: {tono}
- Contexto/Área: {contexto}

El prompt debe seguir todas las mejores prácticas del manual."""
    return prompt

def crear_prompt_imagen(descripcion, estilo, resolucion, ia_destino="Midjourney"):
    if "stable" in ia_destino.lower():
        manual = MANUAL_STABLE_DIFFUSION
    else:
        manual = MANUAL_MIDJOURNEY
    prompt = f"""Usando estas mejores prácticas:
{manual}

Crea un prompt optimizado para {ia_destino} con estas características:
- Descripción: {descripcion}
- Estilo visual: {estilo}
- Resolución/Formato: {resolucion}

El prompt debe seguir todas las mejores prácticas del manual."""
    return prompt

def crear_prompt_universal(descripcion, tipo_tarea, ia_preferida="la más adecuada"):
    todos_los_manuales = f"""
MANUAL CHATGPT:{MANUAL_CHATGPT}
MANUAL MIDJOURNEY:{MANUAL_MIDJOURNEY}
MANUAL STABLE DIFFUSION:{MANUAL_STABLE_DIFFUSION}
MANUAL GEMINI:{MANUAL_GEMINI}
"""
    prompt = f"""Usando el conocimiento de todos estos manuales:
{todos_los_manuales}

Crea el prompt más optimizado posible para esta tarea:
- Descripción: {descripcion}
- Tipo de tarea: {tipo_tarea}
- IA preferida: {ia_preferida}

Aplica las mejores técnicas de todos los manuales que sean relevantes."""
    return prompt


# ————————————————————————————————————————————————
# SECCIÓN 2: DEFINICIÓN DE HERRAMIENTAS PARA CLAUDE
# ————————————————————————————————————————————————

tools = [
    {
        "name": "crear_prompt_texto",
        "description": "Crea un prompt optimizado para IAs de texto como ChatGPT o Gemini, usando las mejores prácticas de cada una.",
        "input_schema": {
            "type": "object",
            "properties": {
                "objetivo": {"type": "string", "description": "Qué quiere lograr el usuario con el prompt"},
                "tono": {"type": "string", "description": "Tono deseado: formal, casual, técnico, creativo"},
                "contexto": {"type": "string", "description": "Área del prompt: marketing, educación, ventas..."},
                "ia_destino": {"type": "string", "description": "Para qué IA es el prompt: ChatGPT, Gemini, etc."}
            },
            "required": ["objetivo", "tono", "contexto"]
        }
    },
    {
        "name": "crear_prompt_imagen",
        "description": "Crea un prompt optimizado para IAs de imagen como Midjourney o Stable Diffusion, usando las mejores prácticas de cada una.",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {"type": "string", "description": "Descripción detallada de la imagen"},
                "estilo": {"type": "string", "description": "Estilo visual: realistic, anime, watercolor..."},
                "resolucion": {"type": "string", "description": "Formato: 4k, portrait, landscape..."},
                "ia_destino": {"type": "string", "description": "Para qué IA es el prompt: Midjourney, Stable Diffusion"}
            },
            "required": ["descripcion", "estilo", "resolucion"]
        }
    },
    {
        "name": "crear_prompt_universal",
        "description": "Usa cuando el usuario no especifica una IA o quiere el mejor prompt posible combinando técnicas de todas las IAs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {"type": "string", "description": "Descripción completa de lo que necesita el usuario"},
                "tipo_tarea": {"type": "string", "description": "Tipo de tarea: texto, imagen, código, análisis..."},
                "ia_preferida": {"type": "string", "description": "IA preferida si el usuario la mencionó"}
            },
            "required": ["descripcion", "tipo_tarea"]
        }
    }
]


# ————————————————————————————————————————————————
# SECCIÓN 3: EL AGENTE
# ————————————————————————————————————————————————

def ejecutar_herramienta(nombre, argumentos):
    if nombre == "crear_prompt_texto":
        return crear_prompt_texto(**argumentos)
    elif nombre == "crear_prompt_imagen":
        return crear_prompt_imagen(**argumentos)
    elif nombre == "crear_prompt_universal":
        return crear_prompt_universal(**argumentos)

def agente(peticion_usuario):
    client = anthropic.Anthropic(api_key="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" \
    "")

    mensajes = [{"role": "user", "content": peticion_usuario}]

    system_prompt = """Eres un experto mundial en crear prompts para IAs.
Tienes acceso a los manuales de mejores prácticas de ChatGPT, Midjourney, Stable Diffusion y Gemini.

Cuando el usuario te pida un prompt:
1. Identifica qué tipo de tarea es (texto, imagen, código, etc.)
2. Identifica si menciona una IA específica
3. Usa la herramienta más adecuada
4. Si no menciona una IA específica, usa crear_prompt_universal
5. Presenta el prompt final de forma clara y lista para copiar y pegar
6. Explica brevemente qué técnicas aplicaste y por qué"""

    print(f"\n🤖 Analizando tu petición con los manuales de todas las IAs...\n")

    while True:
        respuesta = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=system_prompt,
            tools=tools,
            messages=mensajes
        )

        if respuesta.stop_reason == "tool_use":
            mensajes.append({"role": "assistant", "content": respuesta.content})
            resultados = []
            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    print(f"🔧 Aplicando manual de: {bloque.name.replace('crear_prompt_', '').upper()}")
                    resultado = ejecutar_herramienta(bloque.name, bloque.input)
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado
                    })
            mensajes.append({"role": "user", "content": resultados})

        elif respuesta.stop_reason == "end_turn":
            for bloque in respuesta.content:
                if hasattr(bloque, "text"):
                    print("✅ Tu prompt optimizado:\n")
                    print(bloque.text)
            break


# ————————————————————————————————————————————————
# SECCIÓN 4: PROGRAMA PRINCIPAL
# ————————————————————————————————————————————————

if __name__ == "__main__":
    print("=" * 55)
    print("   🚀 AGENTE EXPERTO EN PROMPTS — v2.0")
    print("   📚 ChatGPT | Midjourney | Stable Diffusion | Gemini")
    print("=" * 55)

    while True:
        peticion = input("\n¿Qué prompt necesitas? (o escribe 'salir'): ")
        if peticion.lower() == "salir":
            print("¡Hasta luego!")
            break
        agente(peticion)