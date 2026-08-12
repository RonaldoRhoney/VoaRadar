# CLAUDE.md — Voa Radar

Instruções para quem (humano ou Claude Code) for trabalhar neste repositório.

## Regra fixa: não implementar ideia não pedida

Se, durante o desenvolvimento, surgir uma ideia que pareceria interessante mas não foi pedida (ex: "seria legal ter login"), **não implementar**. Registrar como:

- `Sugestão futura: <ideia>` — quando é uma melhoria possível, não urgente.
- `Problema identificado: <descrição>` — quando é uma limitação/risco arquitetural percebido.

Apresentar essas notas ao usuário (no chat e/ou em [ROADMAP.md](ROADMAP.md)) e deixar a decisão de produto com ele. Isso vale para toda a sessão de desenvolvimento, não só para a tela inicial.

## Documentar por etapa

Este projeto também é portfólio. Cada etapa relevante (decisão de arquitetura, problema encontrado, solução aplicada) deve ficar registrada em [docs/DECISIONS.md](docs/DECISIONS.md) — não só o código final.

## Stack (padrão RhoneyInc)

- **Frontend**: `frontend/` — React + TypeScript + Vite + Tailwind v4 (plugin do Vite, sem `tailwind.config.js`). Roteamento com `react-router-dom` (`BrowserRouter` em `main.tsx`).
- **Backend**: `backend/` — FastAPI, estrutura modular (`app/main.py`, `app/config.py`, `app/models/`, `app/routers/`). Ambiente virtual em `backend/.venv`.
- **Dados mock**: claramente marcados no código como `MOCK DATA` / `*Mock` — nunca confundir com dado real.
- **Rodapé**: segue a skill `footer-padrao` do ecossistema RhoneyInc — 4 colunas fixas (Marca, Produto, RhoneyInc, Legal).

## Convenções

- Cores/tema: tokens Tailwind customizados em `frontend/src/index.css` (`@theme`) — `sky-*` (ação), `night-*` (fundo), `radar-*` (preço/destaque).
- Não usar classes Tailwind fora da escala padrão (ex: `h-8.5`) — usar `[valor]` arbitrário quando necessário.
