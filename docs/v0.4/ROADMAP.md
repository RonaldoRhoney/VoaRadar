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
- [x] FASE 8 — Testes E2E: 7/7 Playwright passando (v0.2/v0.3 sem regressão + v0.4), rodados contra o backend com as chaves reais do Supabase Auth já configuradas. **Fluxo real completo validado manualmente** (curl, não UI — confirmação de e-mail exige clicar num link fora do navegador de teste): cadastro real → `profiles` criado atomicamente → confirmação manual do e-mail de teste (conta descartável, removida depois) → login real → token ES256 validado pelo backend via JWKS → `GET /radars` autenticado (200) → `POST /radars` (Radar real criado) → `python -m scripts.seed_history` → Radar Engine disparou → notificação criada e listada via `GET /notifications`.
- [x] FASE 9 — Revisão manual crítica (não só testes verdes) achou mais 3 problemas reais antes do checklist formal: sino de notificações dessincronizado da página `/notificacoes` (DEC-113), `PUT /radars` sem validar condição no estado final mesclado (DEC-114), Radar com origem=destino sem checagem (DEC-115, migration `0010`). Depois disso, **checklist formal completo da skill `vibe-coding-5-falhas` rodado e passando nos 5 itens** — RLS/grants reconfirmados por introspecção real (10 tabelas), IDOR com 10/10 testes automatizados, permissão-no-front/XSS/chaves expostas todos limpos por grep + Bandit + inspeção do bundle de produção. Detalhe completo em `SECURITY.md` §6. 92/92 pytest, Bandit limpo, 16/16 Vitest, 7/7 E2E.
- [x] FASE 10 — Release `v0.4.0` (2026-08-14, tag cortada em `5a83572`).

**Estado atual**: FASE 0–10 concluídas — v0.4.0 lançada. Backend: `auth.py`/`radars.py`/`notifications.py`/`airports.py`, models, migrations `0004`-`0010` (grants automáticos do Supabase corrigidos em `0008`/DEC-109, `ON DELETE CASCADE` em `0009`/DEC-112, CHECK origem≠destino em `0010`/DEC-115), Radar Engine + cooldown puros e testados, `RadarEvaluationService` ligado ao `FlightCollector` e ao `scripts/seed_history.py`. Frontend: auth (via backend, não supabase-js — DEC-110), Meus Radares (CRUD completo), central de notificações com estado compartilhado (DEC-113), sino no header. `backend/.env` com `SUPABASE_URL`/`SUPABASE_ANON_KEY` reais — não usa mais `SUPABASE_JWT_SECRET` (DEC-111, validação via JWKS).

**Próximo passo**: cortar a tag `v0.4.0`.

## Depois da v0.4.0 (v0.4.x)

- Radar por região (origem → região, não só destino específico).
- "Qualquer destino" — só depois de estratégia de coleta real definida (custo de processamento cresce muito).
- Condições combinadas por Radar (exigiria `radar_conditions` como tabela própria).
- Excluir/arquivar notificações.

## v0.5+ (fora do escopo desta versão)

- Integração real com provedor de voos (Amadeus ou equivalente) — é o que dá sentido a um scheduler/worker de coleta, que a v0.4 deliberadamente não introduz.
- Canais de notificação externos (e-mail, push, Telegram, WhatsApp).
