# Sensitive Info Analyzer (App B)

FastAPI-based AI service that detects, masks, and encrypts sensitive data using RAG (ChromaDB + Gemini).

## 🚀 Features

- Translation-aware analysis
- Gemini API for sensitive detection
- ChromaDB for self-learning via vector search
- Fernet encryption
- Auto-learner: adds new patterns to Chroma over time

## 📦 Requirements

- Python 3.10+
- `requirements.txt`

## 🔐 .env Format (locally only)

GEMINI_API_KEY=your_google_api_key
FERNET_KEY=your_generated_fernet_key

## 🛠 Run Locally

Access: http://localhost:8000/docs

## 🌐 Deploy to Render

1. Push this project to GitHub
2. Create new Render Web Service
3. Use `main:app` as entry point
4. Add env vars:
   - `GEMINI_API_KEY`
   - `FERNET_KEY`

✅ Done!