
import os
import json
import time
import random

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)


schema = {
    "type": "OBJECT",
    "properties": {
        "categoria": {
            "type": "STRING",
            "enum": [
                "incidencia_envio",
                "devolucion",
                "consulta_producto",
                "otro"
            ]
        },
        "prioridad": {
            "type": "STRING",
            "enum": ["alta", "media", "baja"]
        },
        "respuesta_sugerida": {
            "type": "STRING"
        }
    },
    "required": [
        "categoria",
        "prioridad",
        "respuesta_sugerida"
    ]
}


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=schema,
    system_instruction=(
        "Eres un asistente de atención al cliente de una "
        "empresa de comercio internacional. "
        "Clasifica las consultas según su categoría y prioridad. "
        "Redacta una respuesta cordial y profesional en español. "
        "No inventes información sobre pedidos, reembolsos "
        "o políticas de la empresa."
    )
)


def validate_response(data):
    required_fields = {
        "categoria",
        "prioridad",
        "respuesta_sugerida"
    }

    valid_categories = {
        "incidencia_envio",
        "devolucion",
        "consulta_producto",
        "otro"
    }

    valid_priorities = {"alta", "media", "baja"}

    if not isinstance(data, dict):
        raise ValueError("Response must be a JSON object")

    if set(data.keys()) != required_fields:
        raise ValueError("Invalid JSON fields")

    if data["categoria"] not in valid_categories:
        raise ValueError("Invalid category")

    if data["prioridad"] not in valid_priorities:
        raise ValueError("Invalid priority")

    if (not isinstance(data["respuesta_sugerida"], str)
            or not data["respuesta_sugerida"].strip()):
        raise ValueError("Invalid suggested response")

    return data


def analyze_message(message):
    max_attempts = 4

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=message,
                config=config
            )

            if not response.text:
                raise ValueError("Empty response from Gemini")

            data = json.loads(response.text)

            return validate_response(data)

        except errors.APIError as error:
            if error.code not in (408, 429) and not 500 <= error.code < 600:
                raise

            if attempt == max_attempts - 1:
                raise

            backoff_delay = 2 ** attempt
            jitter = random.uniform(0, backoff_delay)
            wait_time = backoff_delay + jitter

            print(
                f"Temporary error {error.code}. "
                f"Retrying in {wait_time:.2f} seconds..."
            )

            time.sleep(wait_time)


def main():
    print("Customer Support Assistant")
    print("--------------------------")

    message = input("Customer message: ").strip()

    if not message:
        print("Please enter a message.")
        return

    try:
        result = analyze_message(message)

        print("\nAnalysis result:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

    except errors.APIError as error:
        print(f"Gemini API error: {error.code}")

    except (ValueError, json.JSONDecodeError) as error:
        print(f"Invalid response: {error}")


if __name__ == "__main__":
    main()
