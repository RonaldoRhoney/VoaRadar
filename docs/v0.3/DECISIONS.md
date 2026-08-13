# Voa Radar v0.3 — Decisões

## DEC-001 — Não reconstruir a v0.2

A v0.3 evolui a fundação existente.

## DEC-002 — PostgreSQL passa a fazer parte da aplicação

**Motivo**: a v0.3 necessita de persistência histórica.

## DEC-003 — Histórico não será sobrescrito

Cada observação é preservada.

## DEC-004 — Destination, Offer e PriceObservation são conceitos diferentes

Continuidade da separação já estabelecida na v0.2 (DEC-009 de `docs/v0.2/DECISIONS.md`).

## DEC-005 — Analytics engine separado da API

## DEC-006 — O frontend não calcula o score

O backend é responsável pela inteligência; o frontend só apresenta.

## DEC-007 — O score não representa previsão

## DEC-008 — Dados insuficientes reduzem a confiança

## DEC-009 — A v0.3 não depende de um provider real específico

**Motivo**: instabilidade recente sinalizada no acesso self-service do Amadeus, e a API de "Cheapest Date Search" deles é baseada em cache pré-computado — dinâmica diferente da busca ao vivo. O motor de inteligência não deve depender de qual fornecedor será usado no futuro.

## DEC-010 — Nenhuma integração de scraping

## DEC-011 — Nenhuma funcionalidade de booking

## DEC-012 — Moeda explícita, nunca assumir BRL permanentemente

## DEC-013 — Banco de dados via Supabase (não Postgres genérico/Docker local)

**Motivo**: decisão do usuário — consistente com o padrão já usado por todo o resto do ecossistema RhoneyInc (MeuPet, MenuFlex, AmaVida...). Resolve a pendência em aberto desde a auditoria da v0.1 (`docs/AUDIT_V0.1.md`, seção "Pendências") sobre onde/como conectar banco de dados.

## Problema encontrado e corrigido — FASE 2 (conexão real)

`alembic upgrade head` falhava com `ValueError: invalid interpolation syntax` ao processar a `DATABASE_URL`. Causa: a senha do banco tem caracteres especiais (`@`) percent-encoded como `%40`, e `Config.set_main_option()` do Alembic passa o valor pelo `configparser`, que interpreta `%` como início de sintaxe de interpolação (`%(nome)s`).

**Solução**: `alembic/env.py` deixou de usar `config.set_main_option("sqlalchemy.url", ...)` + `engine_from_config` (que dependem do `configparser`) e passou a criar a engine diretamente com `sqlalchemy.create_engine(DATABASE_URL, ...)`, lendo a URL direto de `app.core.config` — nunca mais passa pelo parser de `.ini`. Testado de ponta a ponta: `upgrade head` → 5 tabelas criadas no Supabase real → `downgrade -1` limpa tudo → `upgrade head` reaplica sem erro.
