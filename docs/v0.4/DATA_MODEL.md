# Voa Radar v0.4 — Modelo de dados

## 1. Visão geral

```
auth.users (Supabase Auth, gerenciado pelo Supabase)
   │
   ├── profiles (1:1, id compartilhado)
   │
   ├── radars (1:N)
   │     │
   │     └── radar_events (1:N)
   │            │
   │            └── notifications (1:1 por evento, na v0.4.0)
   │
   └── notifications (1:N, via user_id)
```

`airports`, `airlines`, `routes`, `flight_observations`, `price_snapshots` — todas da v0.3, reaproveitadas sem alteração de schema.

## 2. `profiles`

```sql
id          uuid primary key references auth.users(id)
created_at  timestamptz not null default now()
```

Não duplica nada que `auth.users` já guarda (e-mail, senha ficam só no schema `auth` do Supabase). Mínimo absoluto — sem nome, avatar ou qualquer outro campo na v0.4.0 (adicionar sob demanda real, não especulativamente).

## 3. `radars`

```sql
id                        uuid primary key default gen_random_uuid()
user_id                   uuid not null references auth.users(id)
name                      text not null
origin_airport_id         uuid not null references airports(id)
destination_airport_id    uuid not null references airports(id)   -- obrigatório na v0.4.0, sem "qualquer destino"
status                    text not null default 'ACTIVE'            -- ACTIVE | PAUSED
condition_type            text not null                              -- PRICE_BELOW | OPPORTUNITY_CLASSIFICATION
condition_price           numeric                                     -- usado quando condition_type = PRICE_BELOW
condition_classification  text                                        -- usado quando condition_type = OPPORTUNITY_CLASSIFICATION
last_event_price          numeric                                     -- denormalizado, ver ALERT_RULES.md
last_event_at             timestamptz                                 -- denormalizado, ver ALERT_RULES.md
created_at                timestamptz not null default now()
updated_at                timestamptz not null default now()
```

Índice: `(origin_airport_id, destination_airport_id, status)` — é por esse índice que o Radar Engine busca "quais Radares avaliar" quando um novo `price_snapshot` chega numa rota.

`condition_price` e `condition_classification` são mutuamente exclusivos (checagem de aplicação, não constraint de banco — mantém o schema simples; validação real fica no Pydantic schema/service).

**Decisão registrada** (ver `DECISIONS.md` DEC-102): `condition_type` fica como colunas em `radars`, não como tabela `radar_conditions` separada, porque a v0.4.0 só suporta uma condição por Radar. Vira tabela própria no dia em que condições combinadas forem pedidas.

## 4. `radar_events`

```sql
id                  uuid primary key default gen_random_uuid()
radar_id            uuid not null references radars(id)
price_snapshot_id   uuid not null references price_snapshots(id)
price               numeric not null      -- preço no momento do match
score               int                     -- score do Price Intelligence no momento
classification      text                    -- classification do Price Intelligence no momento
created_at          timestamptz not null default now()
```

Append-only. Nunca editado/apagado pelo usuário — é log de auditoria, não estado mutável. Um `radar_event` é criado toda vez que o motor detecta um match, **mesmo quando o cooldown impede a notificação** (ver `ALERT_RULES.md` §2) — assim o histórico de "quando o Radar bateu" fica completo mesmo que nem toda ocorrência vire notificação.

## 5. `notifications`

```sql
id                uuid primary key default gen_random_uuid()
user_id           uuid not null references auth.users(id)
radar_id          uuid not null references radars(id)
radar_event_id    uuid not null references radar_events(id)
type              text not null default 'OPPORTUNITY_FOUND'
title             text not null
message           text not null
read_at           timestamptz
created_at        timestamptz not null default now()
```

`user_id` é denormalizado a partir de `radars.user_id` (evita join extra pra listar notificações do usuário, e simplifica a policy de RLS — ver `SECURITY.md` §3).

## 6. O que fica igual à v0.3

`airports`, `airlines`, `routes`, `flight_observations`, `price_snapshots` — nenhuma alteração de schema. `routes` continua sendo a chave de agrupamento de histórico que o Price Intelligence já usa; `radars` referencia `airports` diretamente (origem/destino), não `routes`, porque um Radar existe antes de necessariamente haver uma `route` com histórico — a relação nasce no motor de avaliação, não no schema.

## 7. Migrations previstas (nomes preliminares, confirmar na fase de implementação)

- `0004_create_profiles.py`
- `0005_create_radars.py`
- `0006_create_radar_events.py`
- `0007_create_notifications.py`

Cada uma nasce com RLS habilitado e policy definida na mesma migration — nunca "criar tabela" e "RLS" em migrations separadas (ver `SECURITY.md` §1, resposta direta ao achado da auditoria de RLS da v0.3).
