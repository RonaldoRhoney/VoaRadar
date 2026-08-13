# Voa Radar v0.3 — Modelo de Dados

> Parte que merece cuidado especial — proposta a ser validada na análise A-K antes de virar migration.

## 1. Objetivo

Persistir observações de preços para permitir análise histórica.

## 2. `airports`

`id`, `code`, `name`, `city`, `country`, `created_at`

## 3. `airlines`

`id`, `code`, `name`, `created_at`

## 4. `routes`

`id`, `origin_airport_id`, `destination_airport_id`, `created_at`

Constraint: `origin != destination`.

## 5. `flight_observations`

`id`, `route_id`, `airline_id`, `departure_date`, `return_date`, `price`, `currency`, `stops`, `duration_minutes`, `provider`, `provider_offer_id`, `observed_at`

## 6. `price_snapshots`

`id`, `flight_observation_id`, `price`, `currency`, `observed_at`

## 7. Contexto de análise

A análise deve considerar o contexto da viagem: origem, destino, data, retorno, passageiros, cabine, escalas. Não comparar ofertas completamente diferentes como se fossem a mesma coisa.

## 8. Índices

Avaliar índices para `route_id`, `departure_date`, `observed_at`, `price`.

## 9. Histórico

Não sobrescrever preços anteriores — cada observação é preservada.

## 10. Auditoria

Todo dado possui timestamp.

## 11. Moeda

Armazenar moeda explicitamente. Não assumir BRL para sempre.

## 12. Provider

Guardar identificação do provider — importante quando houver múltiplas fontes.

## 13. Migration

Usar ferramenta de migration apropriada. Não modificar banco manualmente sem migration.
