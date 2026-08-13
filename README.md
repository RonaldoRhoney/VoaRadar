# Voa Radar

Buscador de passagens aéreas com busca orçamento-primeiro: "tenho X reais, para onde posso viajar?" — e agora também "esse preço é realmente bom?", comparando cada oferta com o histórico observado.

Produto RhoneyInc.

> Estado atual: v0.3.0 ("Price Intelligence") em fechamento, sobre a fundação da v0.1.0 e da v0.2.0 ("Explore"). Primeira versão com banco de dados real (Postgres via Supabase) — histórico de preços persistido e analisado. Ofertas de voo continuam **dados mock** (`FlightProvider`/`MockFlightProvider`) até integração validada com um provedor real.

## Documentação

| Documento | Conteúdo |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Governança do projeto — regras de como o Claude Code (e qualquer dev) deve trabalhar aqui |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | O que é o produto, público, visão v0.1→v1.0 |
| [PRD.md](PRD.md) | Escopo da v0.1 |
| [ROADMAP.md](ROADMAP.md) | Execução da v0.1 à v0.3, passo a passo |
| [docs/v0.1/](docs/v0.1/) | Documentação completa da v0.1 (Contexto, PRD, UX, Arquitetura, Implementação, Critérios de aceite, Roadmap, Decisões) |
| [docs/AUDIT_V0.1.md](docs/AUDIT_V0.1.md) | Auditoria completa da v0.1 (testado, corrigido, pendências, riscos) |
| [docs/v0.2/](docs/v0.2/) | Documentação completa da v0.2 (mesmo formato da v0.1) |
| [docs/v0.3/](docs/v0.3/) | Documentação completa da v0.3 — inclui `DATA_MODEL.md` e `PRICE_INTELLIGENCE.md`, específicos desta versão |

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
pip install -r requirements/dev.txt   # inclui requirements/base.txt + deps de teste
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/health
pytest                                       # roda os testes (não precisam de banco real)
```

### Banco de dados (Supabase/Postgres, desde a v0.3)

Necessário só para os endpoints de Price Intelligence (`/flights/explore` funciona sem banco).

```bash
cp .env.example .env
# edite .env e preencha DATABASE_URL com a connection string do seu projeto Supabase
# (Session pooler, tipo URI — troque postgresql:// por postgresql+psycopg://)
alembic upgrade head                         # cria as tabelas
python -m scripts.seed_history                # popula histórico de exemplo (mock)
```
