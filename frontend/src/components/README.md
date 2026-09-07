# Smart Greenhouse Control System

Course project for Design Patterns and Object-Oriented Techniques (XAMK).

## Prerequisites

- Python 3.11+
- Node.js 20 LTS
- Docker Desktop

## First-time setup

```bash
# 1. Copy environment
cp .env.example .env

# 2. Start PostgreSQL
docker compose up -d

# 3. Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd src
alembic upgrade head

# 4. Frontend
cd ../../frontend
npm install
```

## Daily start

Terminal 1 — database:

```bash
docker compose up -d
```

Terminal 2 — backend:

```bash
cd backend
source .venv/bin/activate
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 3 — frontend:

```bash
cd frontend
npm run dev
```

## URLs

- API: http://localhost:8000
- Scalar: http://localhost:8000/scalar
- OpenAPI: http://localhost:8000/openapi.json
- UI: http://localhost:5173

## Phase order

See [docs/phases/README.md](docs/phases/README.md).