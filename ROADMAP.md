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

**STATUS: FECHADA** (tag `v0.3.0`) — documentação completa em [docs/v0.3/](docs/v0.3/). Objetivo: "esse preço é realmente bom?" — histórico de preços persistido via Supabase, motor de análise (média/mediana/mínimo/máximo/score/confiança) transparente, sem fabricar inteligência artificial. Execução por fases, ver [docs/v0.3/IMPLEMENTATION.md](docs/v0.3/IMPLEMENTATION.md).

- [x] FASE 1 — modelo de dados (`Airport`, `Airline`, `Route`, `FlightObservation`, `PriceSnapshot`) + migration inicial.
- [x] FASE 2 — conectado ao Supabase real, migration aplicada (5 tabelas), rollback testado.
- [x] FASE 3 — `PriceHistoryRepository` (get-or-create + dedup + histórico por rota), testado contra SQLite em memória.
- [x] FASE 4 — `FlightCollector` alimenta o histórico a partir do `MockFlightProvider`; `scripts/seed_history.py` populou o Supabase real (9 observações, idempotência confirmada rodando 2x).
- [x] FASE 5 — Analytics Engine (`app/analytics/`): mínimo/máximo/média/mediana/variação/score/confiança, puro e determinístico, 14 testes (fronteiras de score e confiança, outlier não distorce mediana, dados insuficientes). Validado contra o histórico real da rota BEL→REC (score 100/EXCELLENT pro preço mínimo já visto, confiança LOW com 6 observações).
- [x] FASE 6 — `PriceIntelligenceService` (`app/services/`): combina repository + analytics engine; `analyze_offer(provider_offer_id, current_price)` resolve rota → histórico → análise, `analyze_route` direto por `route_id`. 4 testes, validado contra oferta real do Supabase (`offer-rec-001` → score 100/EXCELLENT).
- [x] FASE 7 — `GET /flights/price-intelligence/{offer_id}?price=X`: 404 amigável pra oferta sem histórico, validação de `price`, 4 testes de API. Achou e corrigiu um bug real de teste (SQLite `:memory:` isolado por thread no `TestClient` — `StaticPool` resolveu).
- [x] FASE 8 — Frontend: `features/price-intelligence/` (hook, view de análise com badge/explicação/stats/confiança, gráfico SVG próprio sem lib), integrado no detalhe da oferta. `history` (série bruta) adicionado ao schema pra viabilizar o gráfico, que o `PRICE_INTELLIGENCE.md` original não previa. Achou e corrigiu mais um bug real de teste (SQLite `:memory:` isolado por thread no `TestClient`). 3 testes de hook novos, validado visualmente (desktop+mobile) contra o Supabase real — R$429 (mínimo já visto) → 🟢 Excelente oportunidade, gráfico renderizando o histórico de verdade.
- [x] FASE 9 — integração confirmada (suite inteira verde, frontend não duplica lógica de negócio do backend).
- [x] FASE 10 — auditoria: regressão v0.2 (2/2 E2E), responsividade, console/network limpos, migrations íntegras, secrets fora do Git. Achou e corrigiu um bug real (`price=inf`/`nan` derrubava a API com 500 cru — corrigido com `allow_inf_nan=False` + teto de valor).
- [x] FASE 11 — documentação (este arquivo, README, PROJECT_CONTEXT, `docs/v0.3/`).
- [x] FASE 12 — release `v0.3.0`.

## Pós-release v0.3.0 — auditoria de segurança (RLS + permissões)

**Achado crítico corrigido**: nenhuma tabela tinha Row Level Security habilitado, e `anon`/`authenticated` (papéis da API REST pública do Supabase) tinham `SELECT/INSERT/UPDATE/DELETE/TRUNCATE` liberados em todas as 5 tabelas — qualquer pessoa com a chave `anon` pública conseguia ler ou apagar o histórico de preço direto pelo Supabase, sem passar pelo backend. Corrigido com a migration `0002` (RLS habilitado + grants revogados nas 5 tabelas), sem nenhum efeito no backend (que acessa como dono da tabela, `rolbypassrls=true`). Regras de negócio reauditadas: confirmado que score/classificação/status de orçamento só existem no backend, frontend só filtra/ordena o que já vem calculado. Detalhe completo em [docs/v0.3/AUDIT_SECURITY.md](docs/v0.3/AUDIT_SECURITY.md) e `docs/v0.3/DECISIONS.md` DEC-021.

## v0.4 — Radar & Alertas

**STATUS: FECHADA** (tag `v0.4.0`, 2026-08-14) — documentação completa em [docs/v0.4/](docs/v0.4/). FASE 0-10 concluídas: modelo Radar, regras de disparo, monitoramento, RLS/segurança, backend (auth real via Supabase, radar engine, evaluation service), frontend (login, Meus Radares, central de notificações), 92/92 pytest, Bandit limpo, 16/16 Vitest, 7/7 E2E, checklist formal das 5 falhas de vibe coding. *(Item corrigido nesta revisão — este arquivo listava "Alertas (v0.4)" como pendente por desatualização, quando já estava lançada.)*

**Extensão pós-release**: Admin padrão (`rhoneyinc@gmail.com`) — **STATUS: CONCLUÍDA** (FASE A DEC-116, FASE B DEC-121, FASE C DEC-120, todas em 2026-08-16/17). `GET /admin/metrics` (só agregados) + painel `/admin` no frontend, login social Google, role decidido só a partir de `profiles`.

## v0.5 — Admin completo, calendário de datas, referência ANAC real

**STATUS: FECHADA** (tag `v0.5.0`, 2026-08-17) — extensão pós-v0.4.0 fechada formalmente. Admin (FASE A/B/C completas), calendário de flexibilidade de datas (DEC-122, resolve DEC-008 da v0.2), `scripts/import_anac_fares.py` funcionando de ponta a ponta com 7 meses de referência real (DEC-123), 27 capitais brasileiras no seletor de Radar (DEC-124), domínio próprio + hub RhoneyInc (DEC-119), 3 bugs reais corrigidos testando em produção (condição de corrida no AdminRoute, CORS do domínio novo, SPA sem rewrite). Investigado e bloqueado por decisão de negócio (não técnica): Open Finance, WhatsApp, provider de oferta real. 103/103 pytest, Bandit limpo, 16/16 Vitest, build ok.

## Próximo

- [x] Deploy (Vercel) — frontend e backend. **Concluído 2026-08-16** (DEC-118): `voaradar-api` (backend) e `voaradar-frontend` (frontend), ambos em produção, CORS liberado pro domínio real, `ssoProtection` desativado em ambos os projetos. Só URLs `*.vercel.app` padrão por enquanto — domínio próprio `voaradar.rhoneyinc.com` e entrada no hub/rodapés seguem pendentes.
- [x] **"RhoneyInc Zero-Cost API First"** (2026-08-16/17, DEC-117/118/123) — `AnacFareProvider`/`FareReferenceProvider` implementado e em produção. `scripts/import_anac_fares.py` **concluído** (DEC-123): schema real do CSV finalmente verificado baixando um arquivo de verdade, script roda o fluxo completo (postback ASP.NET → CSV → agregação ponderada → upsert). Rodado pra janeiro/2025 em produção: 20 rotas importadas, `anac_reference` confirmado preenchido no endpoint real. Falta só rodar pra mais meses (execução manual, não agendada ainda).
- [x] Calendário de flexibilidade de datas (DEC-008 de `docs/v0.2/DECISIONS.md`). **Concluído 2026-08-17** (DEC-122): calendário de preço por dia na tela de detalhe da oferta, `GET /flights/calendar`, ainda mock (determinístico, não tarifa real).
- [x] Admin — FASE C (login social Google). **Concluído 2026-08-17** (DEC-120).
- [x] Admin — FASE B (painel de métricas). **Concluído 2026-08-17** (DEC-121).
- [ ] Provider de oferta real (Amadeus Enterprise, Duffel, outro) — `BLOCKED` até aprovação explícita de orçamento, fora do escopo até haver decisão de negócio. Investigação real registrada em `docs/OFFER_PROVIDER_INVESTIGATION.md` (2026-08-17): Duffel free tier só dá preço fictício (companhia fake "Duffel Airways"), cota de busca grátis é proporcional a reserva confirmada (zero reserva = zero busca grátis); Kiwi Tequila fechou cadastro self-service, exige 50k MAU. Nenhum caminho zero-custo real encontrado, mesma conclusão estrutural do Open Finance.
- [ ] Inteligência artificial / recomendações (v0.5).

## Sugestões futuras registradas (não implementadas)

- Autenticação de usuário / contas / buscas salvas / alertas de preço.
- Domínio próprio `voaradar.rhoneyinc.com` + entrada no hub RhoneyInc e nos rodapés dos produtos-irmãos.
- Checklist "novo app no ar" da RhoneyInc deveria incluir o passo de desativar `ssoProtection` via API da Vercel — todo projeto novo nasce com isso ligado, bloqueando acesso público mesmo com build e env vars corretos (achado real do deploy do Voa Radar, DEC-118).
