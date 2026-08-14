# Voa Radar v0.4 — Arquitetura

## 1. Evolução

```
v0.3:  Provider → Collector → Persistence → Analytics → API → Frontend
v0.4:  ... → Persistence → Analytics → Radar Engine → Radar Events → Notifications → API → Frontend
                                              ↑
                                    Auth (Supabase Auth + JWT)
```

## 2. Backend — novos módulos

```
backend/
└── app/
    ├── api/
    │   ├── auth.py            # novo — endpoints delegam ao Supabase Auth, validam JWT
    │   ├── radars.py          # novo
    │   └── notifications.py   # novo
    ├── core/
    │   └── auth.py            # novo — dependency que valida JWT e extrai user_id
    ├── models/
    │   ├── radar.py           # novo
    │   ├── radar_event.py     # novo
    │   └── notification.py    # novo
    ├── repositories/
    │   ├── radar_repository.py        # novo
    │   └── notification_repository.py # novo
    ├── radar_engine/          # novo — motor puro, mesmo padrão de analytics/
    │   └── engine.py
    ├── services/
    │   └── radar_evaluation_service.py  # novo — orquestra repository + radar_engine
    ├── analytics/              # v0.3, reaproveitado sem alteração
    ├── providers/               # v0.2/v0.3, reaproveitado sem alteração
    └── main.py
```

## 3. Auth

Supabase Auth é o provedor (mesmo projeto Supabase já usado pro banco — não introduz fornecedor novo). O backend nunca implementa cadastro/login por conta própria: chama a API do Supabase Auth (via SDK ou REST) e, para requisições autenticadas, valida o JWT recebido no header `Authorization` contra o JWKS do projeto.

`user_id` do usuário autenticado só existe no backend como resultado dessa validação — nunca é lido de body/query param de requisição (defesa de raiz contra IDOR, ver `SECURITY.md`).

## 4. Radar Engine

Função pura, mesmo princípio do `analytics/engine.py` (v0.3 DEC-018): recebe configuração do Radar + preço novo + resultado do Price Intelligence já calculado, devolve "disparou ou não" de forma determinística, sem I/O. Testável isoladamente com dados sintéticos, sem banco.

## 5. Radar Evaluation Service

Orquestra: busca Radares ativos compatíveis com a rota (repository) → chama o Radar Engine pra cada um → aplica a regra de cooldown (`ALERT_RULES.md`) → grava `radar_event` + `notification` quando dispara. Mesma divisão de responsabilidade que `PriceIntelligenceService` já usa entre repository e analytics engine.

## 6. Gatilho de avaliação

Chamado dentro do mesmo fluxo que já persiste um novo `price_snapshot` (`PriceHistoryRepository.record_observation`, v0.3) — orientado a evento, não por polling. Ver `RADAR_ENGINE.md` §3 para o risco de acoplamento registrado.

## 7. Frontend — novos módulos

```
frontend/src/
├── features/
│   ├── auth/              # novo — login, cadastro, sessão
│   ├── radars/             # novo — CRUD de Radar
│   └── notifications/      # novo — central de notificações
├── services/
│   └── supabaseClient.ts   # novo — só para Auth (sessão/token), dados de negócio continuam via backend
```

O frontend fala com o Supabase Auth diretamente pra sessão/login (padrão do SDK), mas **todo dado de negócio** (Radares, eventos, notificações) continua passando pelo backend FastAPI — não vira acesso direto do frontend ao Postgres via PostgREST. RLS funciona como segunda camada de defesa, não como única barreira (ver `SECURITY.md` §2).

## 8. Sem worker/scheduler novo

Confirmado como decisão explícita (não omissão): a v0.4.0 não introduz nenhum processo em background. "Monitorar" = avaliar Radares no mesmo request que grava uma observação nova. Ver `DECISIONS.md` DEC-104 para o racional completo e o gatilho de reavaliação futura.

## 9. Princípio mantido

Regra de negócio nunca no frontend — o frontend só lista Radares/notificações e reage ao que o backend já decidiu (continuidade direta do princípio já auditado na v0.3, `AUDIT_SECURITY.md`).
