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
