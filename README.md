# Little Lamb Translator 🐑

Aplicación desarrollada como prueba de concepto para automatizar tareas de atención al cliente utilizando modelos de inteligencia artificial.

## Funcionalidades

### Frontend
- Traducción de inglés a español y viceversa.
- Modelos de Hugging Face ejecutados directamente en el navegador.
- Detección de WebGPU con alternativa WASM.
- Interfaz interactiva con indicadores de estado.

### Backend
- Análisis de consultas mediante la API de Gemini.
- Clasificación por categoría y prioridad.
- Generación de respuestas sugeridas en español.
- Resultados estructurados mediante JSON Schema.
- Gestión de errores temporales con retroceso exponencial y jitter.

## Tecnologías

- HTML5, CSS3 y JavaScript
- Hugging Face Transformers.js
- Python
- Google Gemini API
- python-dotenv

## Instalación

1. Clonar el repositorio.
2. Crear un entorno virtual:

   `python -m venv .venv`

3. Activarlo en Windows:

   `.venv\Scripts\activate`

4. Instalar las dependencias:

   `pip install -r requirements.txt`

5. Crear un archivo `.env` siguiendo `.env.example` e introducir la API key de Gemini.

## Ejecución

**Frontend:** abrir `index.html` mediante Live Server. La primera carga de cada modelo requiere conexión a Internet para su descarga.

**Backend:** ejecutar `python main.py` desde la terminal.

## Seguridad

La clave de Gemini se almacena en un archivo `.env` que está excluido del repositorio mediante `.gitignore`. No se utiliza la clave en el frontend.