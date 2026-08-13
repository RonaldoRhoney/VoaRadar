# Roadmap — Voa Radar

Este arquivo é o log de execução do projeto (o que foi feito, passo a passo). Documentação completa por versão em [docs/v0.1/](docs/v0.1/), [docs/v0.2/](docs/v0.2/) e [docs/v0.3/](docs/v0.3/) (Contexto, PRD, UX, Arquitetura, Implementação, Critérios de aceite, Roadmap, Decisões — mesmo formato em todas). Auditoria completa da v0.1 em [docs/AUDIT_V0.1.md](docs/AUDIT_V0.1.md).

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

## v0.2 — Explore

- [x] Contrato `Destination`/`Offer` — um destino pode ter várias ofertas, cada oferta com id próprio (`docs/v0.2/DECISIONS.md` DEC-009).
- [x] `MockFlightProvider` expandido: 4 destinos, 2–3 ofertas cada, com data, duração, escalas, companhia.
- [x] `ExploreService`: classifica `within_budget`/`near_budget`, ordena, marca `highlight: "best_price"` sem fabricar índice de oportunidade (DEC-010).
- [x] Endpoint `POST /flights/explore` substituindo `/flights/budget-search`.
- [x] Frontend: `features/explore/` (form com passageiros, cards, filtros, ordenação), detalhe da oferta por id (não mais reconstruído via query string solta).
- [x] Estado "nenhum resultado" sugerindo a opção mais barata acima do orçamento (`near_budget`).
- [x] Testes: 10 backend (pytest), 13 frontend (Vitest), 2 E2E (Playwright) — todos passando.
- [x] Responsividade validada em mobile (390px), tablet (768px) e desktop (1280px).

Divergências conscientes do PRD original, todas registradas em [docs/v0.2/DECISIONS.md](docs/v0.2/DECISIONS.md): painel de filtros único em vez de sidebar+bottom sheet (DEC-011), filtro de escalas simplificado (DEC-012), sem filtro de período (DEC-013), margem de "próximo do orçamento" fixa em R$ 100 (DEC-014).

**v0.2 está funcionalmente fechada**, ainda 100% mock, sem deploy.

## v0.3 — Price Intelligence

**STATUS: EM ANDAMENTO** — documentação completa em [docs/v0.3/](docs/v0.3/). Objetivo: "esse preço é realmente bom?" — histórico de preços persistido via Supabase, motor de análise (média/mediana/mínimo/máximo/score/confiança) transparente, sem fabricar inteligência artificial. Execução por fases, ver [docs/v0.3/IMPLEMENTATION.md](docs/v0.3/IMPLEMENTATION.md).

- [x] FASE 1 — modelo de dados (`Airport`, `Airline`, `Route`, `FlightObservation`, `PriceSnapshot`) + migration inicial.
- [x] FASE 2 — conectado ao Supabase real, migration aplicada (5 tabelas), rollback testado.
- [x] FASE 3 — `PriceHistoryRepository` (get-or-create + dedup + histórico por rota), testado contra SQLite em memória.
- [x] FASE 4 — `FlightCollector` alimenta o histórico a partir do `MockFlightProvider`; `scripts/seed_history.py` populou o Supabase real (9 observações, idempotência confirmada rodando 2x).
- [ ] FASE 5 em diante — analytics engine, price intelligence service, API, frontend.

## Próximo

- [ ] Provisionar Supabase dedicado + admin padrão (`rhoneyinc@gmail.com`) — primeira vez que o projeto conecta banco de dados (v0.3).
- [ ] Deploy (Vercel) — frontend e backend. **Lembrete da auditoria**: `CORS_ORIGINS` no backend hoje só libera `http://localhost:5173` — precisa incluir o domínio real no deploy, senão o frontend em produção não consegue falar com a API (testado: o build de produção rodando em outra porta local já é bloqueado por CORS).
- [ ] Integração com fonte real de dados de voo via `FlightProvider` (Amadeus for Developers, sandbox, ou outro — decisão adiada por instabilidade recente sinalizada no acesso self-service do Amadeus, ver `docs/v0.3/DECISIONS.md` DEC-009).
- [ ] Calendário completo de flexibilidade de datas (DEC-008 de `docs/v0.2/DECISIONS.md`).
- [ ] Alertas (v0.4).
- [ ] Inteligência artificial / recomendações (v0.5).

## Sugestões futuras registradas (não implementadas)

- Autenticação de usuário / contas / buscas salvas / alertas de preço.
- Deploy do backend FastAPI na Vercel via runtime Python (alternativa a outro host).
