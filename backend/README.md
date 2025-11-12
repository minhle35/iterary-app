# Backend API

FastAPI backend for the Iterary App.

## Setup

1. Install dependencies using `uv`:
```bash
uv sync
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Start the development server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

