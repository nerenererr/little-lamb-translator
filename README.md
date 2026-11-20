# Little Lamb Translator 🐑

A proof-of-concept application developed for an international e-commerce company to improve customer support using artificial intelligence.

The project combines a browser-based translator with a Python customer support assistant powered by Google's Gemini API.

## Features

### Frontend — Translation

- English-to-Spanish and Spanish-to-English translation.
- Local inference using Hugging Face Transformers.js.
- WebGPU acceleration with WebAssembly (WASM) fallback.
- Language switching button.
- Loading, translation and error status messages.
- Custom storybook-inspired interface.

### Backend — Customer Support

- Customer message analysis using Google Gemini.
- Automatic classification into four categories:
  - `incidencia_envio`
  - `devolucion`
  - `consulta_producto`
  - `otro`
- Priority classification: `alta`, `media`, `baja`.
- Suggested professional responses in Spanish.
- Structured JSON output using JSON Schema.
- Exponential backoff with jitter for temporary API errors.

## Technologies

**Frontend:** HTML5, CSS3, JavaScript, Transformers.js.

**Backend:** Python, Google GenAI SDK, python-dotenv.

## Project Structure

```text
ud2-customer-support/
├── index.html
├── style.css
├── script.js
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone REPOSITORY_URL
cd ud2-customer-support
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

## How to Run

### Frontend

Open `index.html` using the Live Server extension in Visual Studio Code.

Select the translation direction, enter a message and click **Translate**.

The translation models run locally in the browser. An internet connection is required for the initial download of the models.

### Backend

Run the following command:

```bash
python main.py
```

Enter a customer message when prompted.

The program will return a JSON object containing the category, priority and suggested response.

## Security

The Gemini API key is stored in a local `.env` file and is never included in the frontend.

The `.gitignore` file excludes `.env` and `.venv/` from the Git repository.

## Academic Context

Developed for UD02 — Machine Learning and AI API Integration, as part of the Web Application Development (DAW) coursework.