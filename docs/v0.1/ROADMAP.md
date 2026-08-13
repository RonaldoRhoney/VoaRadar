# Voa Radar v0.1 — Roadmap de execução

> Log de execução da v0.1, passo a passo. Roadmap de versões (v0.1 → v1.0) em [../../PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) e [../../ROADMAP.md](../../ROADMAP.md) (visão completa, todas as versões).

## v0.1 — Fundação + interface + busca com mock data

**STATUS: CONCLUÍDA** (tag `v0.1.0`)

- [x] Estrutura do repositório + repo GitHub próprio.
- [x] Frontend: Vite + React + TS + Tailwind, identidade visual e layout responsivo (header/footer padrão RhoneyInc).
- [x] Tela prioritária: busca por orçamento (Home) → lista de destinos dentro do valor → detalhe da oportunidade.
- [x] Backend: FastAPI com health check, config, endpoint de busca por orçamento.
- [x] Arquitetura modular (seção 11 do `CLAUDE.md`): backend em `api/`, `core/`, `schemas/`, `services/`, `providers/`, `tests/`; frontend em `components/`, `pages/`, `features/`, `services/`, `types/`, `utils/`, `tests/`.
- [x] `FlightProvider` abstrato + `MockFlightProvider` — arquitetura pronta para múltiplos provedores futuros, sem acoplar a nenhum ainda.
- [x] Frontend conectado ao backend real (`services/api.ts` + hook `useBudgetSearch`), não mais mock local.
- [x] Estados de carregamento, vazio e erro amigável na tela de resultados — validados contra um cenário real (backend derrubado de propósito).
- [x] Testes: 5 backend (`pytest`), 3 frontend (Vitest), 1 E2E (Playwright) — todos passando.
- [x] Responsividade validada (desktop 1280px + mobile 390px) com capturas reais do app.
- [x] `SearchForm`/`InspireMe` (fluxo clássico origem/destino/data) removidos — não faziam parte da experiência prioritária.
- [x] Auditoria completa — 7 problemas encontrados e corrigidos (ver [../AUDIT_V0.1.md](../AUDIT_V0.1.md)).

**v0.1 fechada**, rodando só local, sem deploy — deploy fica para depois da v0.2.
