# Voa Radar

Buscador de passagens aéreas com busca orçamento-primeiro: você diz quanto quer gastar, de onde sai e quando — a gente sugere destinos que cabem no valor.

Produto RhoneyInc.

> Estado atual: v0.1.0 concluída e auditada (tag `v0.1.0`). v0.2 ("Explore") em planejamento. **Dados mock** em todas as versões até integração validada com um provedor real.

## Documentação

| Documento | Conteúdo |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Governança do projeto — regras de como o Claude Code (e qualquer dev) deve trabalhar aqui |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | O que é o produto, público, visão v0.1→v1.0 |
| [PRD.md](PRD.md) | Escopo da v0.1 |
| [ROADMAP.md](ROADMAP.md) | Execução da v0.1, passo a passo |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Diário de decisões técnicas da v0.1 |
| [docs/AUDIT_V0.1.md](docs/AUDIT_V0.1.md) | Auditoria completa da v0.1 (testado, corrigido, pendências, riscos) |
| [docs/v0.2/](docs/v0.2/) | Planejamento completo da v0.2 (Contexto, PRD, UX, Arquitetura, Implementação, Critérios de aceite, Roadmap, Decisões) |

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
pytest                                       # roda os testes
```
