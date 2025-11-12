# Project Setup Guide

This guide will help you set up the Iterary App development environment.

## Prerequisites

- Node.js 20+ and npm
- Python 3.13+
- `uv` package manager (install from https://github.com/astral-sh/uv)
- Docker and Docker Compose (for local databases)

## Quick Start

### 1. Start Docker Services (PostgreSQL & Redis)

```bash
cd docker
docker compose up -d postgres redis
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379

**Or run everything in Docker (backend + frontend + databases):**
```bash
cd docker
docker compose up --build -d
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies (uv will create a virtual environment automatically)
uv sync

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run the backend
make dev
# Or directly: uv run uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Project Structure

```
iterary-app/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Core configuration
│   │   ├── models/    # Database models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   ├── Dockerfile.backend
│   ├── Makefile
│   ├── pyproject.toml # uv project file
│   └── uv.lock        # uv lock file
├── frontend/          # React 18 + TypeScript frontend
│   ├── src/
│   ├── Dockerfile.frontend
│   ├── package.json
│   └── vite.config.ts
├── docker/            # Docker configuration
│   └── docker-compose.yml
└── README.md
```

## Development Workflow

### Option 1: Local Development (Recommended for active coding)

1. Start Docker services: `cd docker && docker compose up -d postgres redis`
2. Start backend: `cd backend && make dev`
3. Start frontend: `cd frontend && npm run dev`

### Option 2: Full Docker Setup

1. Start everything: `cd docker && docker compose up --build -d`
2. Access:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `OPENAI_API_KEY`: OpenAI API key
- `MAPBOX_ACCESS_TOKEN`: Mapbox access token

### Frontend
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
- `VITE_MAPBOX_ACCESS_TOKEN`: Mapbox access token

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS
- React Query
- Socket.IO client
- Mapbox GL

### Backend
- FastAPI (Python 3.13)
- SQLAlchemy ORM
- Pydantic + pydantic-settings
- Celery
- Socket.IO
- `uv` for package management
- Makefile for convenient commands (`make dev`)

### Infrastructure
- Docker & Docker Compose
- PostgreSQL
- Redis

