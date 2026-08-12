# Roadmap — Voa Radar

Log detalhado de decisões/problemas em [docs/DECISIONS.md](docs/DECISIONS.md). Visão de versões (v0.1 → v1.0) em [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md). Auditoria completa da v0.1 em [docs/AUDIT_V0.1.md](docs/AUDIT_V0.1.md).

## v0.1 — Fundação + interface + busca com mock data

- [x] Estrutura do repositório + repo GitHub próprio.
- [x] Frontend: Vite + React + TS + Tailwind, identidade visual e layout responsivo (header/footer padrão RhoneyInc).
- [x] Tela prioritária: busca por orçamento (Home) → lista de destinos dentro do valor → detalhe da oportunidade.
- [x] Backend: FastAPI com health check, config, endpoint de busca por orçamento.
- [x] Arquitetura modular (seção 11 do `CLAUDE.md`): backend em `api/`, `core/`, `schemas/`, `services/`, `providers/`, `tests/`; frontend em `components/`, `pages/`, `features/`, `services/`, `types/`, `utils/`, `tests/`.
- [x] `FlightProvider` abstrato + `MockFlightProvider` — arquitetura pronta para múltiplos provedores futuros (Amadeus, Duffel, ...), sem acoplar a nenhum ainda.
- [x] Frontend conectado ao backend real (`services/api.ts` + hook `useBudgetSearch`), não mais mock local.
- [x] Estados de carregamento, vazio e erro amigável na tela de resultados — validados contra um cenário real (backend derrubado de propósito).
- [x] Testes: 4 unitários/API no backend (`pytest`), 3 unitários no frontend (Vitest), 1 E2E ponta a ponta (Playwright) — todos passando.
- [x] Responsividade validada (desktop 1280px + mobile 390px) com capturas reais do app.
- [x] `SearchForm`/`InspireMe` (fluxo clássico origem/destino/data) removidos — não faziam parte da experiência prioritária.

**v0.1 está funcionalmente fechada** (frontend + backend + integração + testes + docs), rodando só local, sem deploy — deploy é item de v0.2 (ver [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)).

## Próximo (v0.2 em diante, sem decisão de quando)

- [ ] Deploy (Vercel) — frontend e backend.
- [ ] Provisionar Supabase dedicado + admin padrão (`rhoneyinc@gmail.com`).
- [ ] Explorar destinos (v0.2, conforme visão do produto).
- [ ] Integração com fonte real de dados de voo via `FlightProvider` (Amadeus for Developers, sandbox) — v0.2/v0.3.
- [ ] Histórico e análise de preços (v0.3).
- [ ] Alertas (v0.4).
- [ ] Inteligência artificial (v0.5).

## Sugestões futuras registradas (não implementadas)

- Autenticação de usuário / contas / buscas salvas / alertas de preço.
- Deploy do backend FastAPI na Vercel via runtime Python (alternativa a outro host).
