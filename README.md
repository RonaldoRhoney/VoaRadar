# Voa Radar

Buscador de passagens aéreas com busca orçamento-primeiro: você diz quanto quer gastar, de onde sai e quando — a gente sugere destinos que cabem no valor.

Produto RhoneyInc. Contexto completo em [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), escopo em [PRD.md](PRD.md), progresso em [ROADMAP.md](ROADMAP.md), decisões técnicas em [docs/DECISIONS.md](docs/DECISIONS.md).

> Estado atual: MVP visual com **dados mock** (frontend e backend), sem integração com fonte real de dados de voo ainda.

## Frontend

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/health
```
