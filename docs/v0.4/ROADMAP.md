# Voa Radar v0.4 — Roadmap

## Fases (definição → implementação)

- [x] FASE 0 — Auditar estado real da v0.3 (reconfirmado: 44/44 testes, RLS ok, tag `v0.3.0`, 2 commits de segurança pós-tag ainda sem `v0.3.1` cortada).
- [x] FASE 1 — Definir modelo Radar (`DATA_MODEL.md`).
- [x] FASE 2 — Definir regras de disparo (`ALERT_RULES.md`).
- [x] FASE 3 — Definir arquitetura do monitoramento (`ARCHITECTURE.md`, `RADAR_ENGINE.md`).
- [x] FASE 4 — Definir segurança/RLS (`SECURITY.md`).
- [x] FASE 5 — Implementar backend (auth, models, migrations, radar engine, evaluation service, API). 84/84 testes passando, Bandit limpo, migrations 0004-0008 aplicadas e verificadas no Supabase real (RLS + grants corretos, rollback testado).
- [ ] FASE 6 — Implementar interface (login/cadastro, Meus Radares, criar/editar Radar).
- [ ] FASE 7 — Central de notificações (backend concluído nesta FASE 5; falta frontend).
- [ ] FASE 8 — Testes E2E (unitários/integração/API já cobertos na FASE 5; falta E2E de ponta a ponta via navegador).
- [ ] FASE 9 — Auditoria (skill `vibe-coding-5-falhas` completa, com itens 2 e 3 aplicáveis).
- [ ] FASE 10 — Release `v0.4.0`.

**Estado atual**: FASE 0–5 concluídas. Backend completo: `auth.py`/`radars.py`/`notifications.py`, models, migrations `0004`-`0008` (incluindo correção de achado real de segurança — grants automáticos do Supabase, ver `SECURITY.md` §6/`DECISIONS.md` DEC-109), Radar Engine + cooldown puros e testados, `RadarEvaluationService` ligado ao `FlightCollector`. Próximo passo: FASE 6 (frontend).

## Depois da v0.4.0 (v0.4.x)

- Radar por região (origem → região, não só destino específico).
- "Qualquer destino" — só depois de estratégia de coleta real definida (custo de processamento cresce muito).
- Condições combinadas por Radar (exigiria `radar_conditions` como tabela própria).
- Excluir/arquivar notificações.

## v0.5+ (fora do escopo desta versão)

- Integração real com provedor de voos (Amadeus ou equivalente) — é o que dá sentido a um scheduler/worker de coleta, que a v0.4 deliberadamente não introduz.
- Canais de notificação externos (e-mail, push, Telegram, WhatsApp).
