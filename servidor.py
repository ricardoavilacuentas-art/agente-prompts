from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

@app.route('/generar', methods=['POST'])
def generar():
    datos = request.json
    api_key = datos.get('apiKey')
    mensaje = datos.get('mensaje')
    sistema = datos.get('sistema')

    print("API Key recibida:", api_key[:20] if api_key else "NINGUNA")
    print("Mensaje recibido:", mensaje[:50] if mensaje else "NINGUNO")

    system_prompt = """Eres un ingeniero experto mundial en crear y perfeccionar prompts para IAs.

Tu objetivo es diseñar el mejor prompt posible para la tarea que el usuario necesita.

MANUALES DE MEJORES PRÁCTICAS:

CHATGPT/GPT-4: Asigna roles específicos. Especifica formato de salida. Usa ejemplos concretos. Define el tono. Divide tareas en pasos. Pide razonamiento paso a paso.

CLAUDE: Usa etiquetas XML (<contexto>, <tarea>, <formato>). Pide pensamiento paso a paso. Combina instrucciones positivas y negativas. Proporciona contexto amplio.

MIDJOURNEY: Estructura: [sujeto], [descripción], [entorno], [estilo], [iluminación], [calidad]. Parámetros: --ar 16:9 --v 6 --q 2. Prompts en inglés.

STABLE DIFFUSION: Palabras de calidad: masterpiece, best quality, ultra-detailed. Prompts negativos: (deformed, bad anatomy, blurry:1.4). Pondera palabras: (beautiful eyes:1.3).

GEMINI: Sé conversacional. Proporciona contexto amplio. Combina rol + tarea + formato.

CLAUDE COPILOT: Especifica lenguaje y versión. Describe claramente la función. Incluye casos de uso. Pide comentarios en el código.

CÓMO DEBES COMPORTARTE:

1. Cuando el usuario describe lo que necesita, SIEMPRE haz entre 2 y 4 preguntas clave antes de generar el prompt. Ejemplos de preguntas útiles:
   - ¿Para qué IA es el prompt?
   - ¿Cuál es el tono deseado?
   - ¿Quién es la audiencia?
   - ¿Qué formato quieres en la respuesta?
   - ¿Hay algo que el prompt NO debe incluir?

2. Cuando el usuario ya responde tus preguntas, genera el prompt optimizado completo y listo para copiar.

3. Cuando el usuario te da un prompt existente para mejorar, analízalo, identifica sus debilidades y entrégale una versión mejorada explicando qué cambiaste y por qué.

4. Después de generar cada prompt, pregunta: ¿Quieres ajustar algo o perfeccionarlo más?

5. Nunca generes un prompt genérico. Siempre busca el máximo nivel de detalle y precisión."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        mensajes = datos.get('historial', [])
        if not mensajes:
            mensajes = [{"role": "user", "content": mensaje}]
        
        respuesta = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=mensajes
        )
        return jsonify({"resultado": respuesta.content[0].text})
    except Exception as e:
        print("ERROR DETALLADO:", str(e))
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=8081)
