# Voa Radar v0.4 — Roadmap

## Fases (definição → implementação)

- [x] FASE 0 — Auditar estado real da v0.3 (reconfirmado: 44/44 testes, RLS ok, tag `v0.3.0`, 2 commits de segurança pós-tag ainda sem `v0.3.1` cortada).
- [x] FASE 1 — Definir modelo Radar (`DATA_MODEL.md`).
- [x] FASE 2 — Definir regras de disparo (`ALERT_RULES.md`).
- [x] FASE 3 — Definir arquitetura do monitoramento (`ARCHITECTURE.md`, `RADAR_ENGINE.md`).
- [x] FASE 4 — Definir segurança/RLS (`SECURITY.md`).
- [x] FASE 5 — Implementar backend (auth, models, migrations, radar engine, evaluation service, API). 84/84 testes passando, Bandit limpo, migrations 0004-0008 aplicadas e verificadas no Supabase real (RLS + grants corretos, rollback testado).
- [x] FASE 6 — Implementar interface (login/cadastro, Meus Radares, criar/editar Radar, sino de notificações no header). `tsc`/oxlint limpos, 16/16 Vitest, build de produção ok.
- [x] FASE 7 — Central de notificações (backend da FASE 5 + página `/notificacoes` e sino no header desta FASE 6).
- [x] FASE 8 — Testes E2E de fumaça (rotas protegidas, renderização, tratamento de erro amigável) — 7/7 Playwright passando (v0.2/v0.3 sem regressão + v0.4). Fluxo real de cadastro/login **não foi validado com credenciais reais do Supabase Auth** — `SUPABASE_URL`/`ANON_KEY`/`JWT_SECRET` ainda não preenchidos em `backend/.env`, ver pendência abaixo.
- [ ] FASE 9 — Auditoria (skill `vibe-coding-5-falhas` completa, com itens 2 e 3 aplicáveis). Reconfirmado parcialmente durante a FASE 5-6 (grep de permissão-no-front/XSS limpo no código novo, matriz IDOR testada) — falta a passada formal de FASE 9 com o checklist completo antes do release.
- [ ] FASE 10 — Release `v0.4.0`.

**Estado atual**: FASE 0–8 concluídas. Backend: `auth.py`/`radars.py`/`notifications.py`/`airports.py`, models, migrations `0004`-`0008` (incluindo correção de achado real de segurança — grants automáticos do Supabase, ver `SECURITY.md` §6/`DECISIONS.md` DEC-109), Radar Engine + cooldown puros e testados, `RadarEvaluationService` ligado ao `FlightCollector`. Frontend: auth (via backend, não supabase-js — DEC-110), Meus Radares (CRUD completo), central de notificações, sino no header.

**Pendência bloqueante pro teste real de ponta a ponta**: preencher `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET` em `backend/.env` (ver painel Supabase > Settings > API) — sem isso, `/auth/signup` e `/auth/login` respondem 503 amigável (testado e funcionando como esperado), mas o cadastro/login real nunca foi exercitado contra o Supabase Auth de verdade. Próximo passo: usuário preencher essas chaves, depois validar manualmente cadastro → login → criar Radar → disparo → notificação, antes da FASE 9.

## Depois da v0.4.0 (v0.4.x)

- Radar por região (origem → região, não só destino específico).
- "Qualquer destino" — só depois de estratégia de coleta real definida (custo de processamento cresce muito).
- Condições combinadas por Radar (exigiria `radar_conditions` como tabela própria).
- Excluir/arquivar notificações.

## v0.5+ (fora do escopo desta versão)

- Integração real com provedor de voos (Amadeus ou equivalente) — é o que dá sentido a um scheduler/worker de coleta, que a v0.4 deliberadamente não introduz.
- Canais de notificação externos (e-mail, push, Telegram, WhatsApp).
