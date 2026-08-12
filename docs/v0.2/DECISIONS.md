# Voa Radar v0.2 — Decisões

## DEC-001 — Não reconstruir a v0.1

A v0.2 utilizará a fundação existente.

**Motivo**: a v0.1 foi auditada e aprovada (ver [../AUDIT_V0.1.md](../AUDIT_V0.1.md)).

## DEC-002 — Mock Provider continua

A v0.2 continuará utilizando `MockFlightProvider`.

**Motivo**: a UX precisa ser validada antes da integração com provedores reais.

## DEC-003 — Provider abstraction

A aplicação continuará utilizando `FlightProvider`.

**Motivo**: permitir múltiplos fornecedores futuramente sem acoplamento.

## DEC-004 — Sem PostgreSQL definitivo

A v0.2 não implementará persistência completa.

**Motivo**: histórico e usuários pertencem a versões futuras.

## DEC-005 — Orçamento como ponto central

A experiência Explore deve partir do orçamento.

**Motivo**: esse é o principal diferencial do Voa Radar.

## DEC-006 — Mobile-first

A experiência será desenvolvida priorizando dispositivos móveis.

**Motivo**: grande parte dos usuários utilizará smartphones.

## DEC-007 — Não implementar funcionalidades futuras

IA, alertas, autenticação e API real permanecem fora da v0.2.

**Motivo**: controle de escopo e qualidade.

## DEC-008 — Período simplificado nesta primeira implementação

Em vez de implementar "mês específico + intervalo + datas flexíveis" simultaneamente (como o PRD original de v0.2 sugere em 3.3), a primeira implementação prioriza **mês + flexibilidade básica**.

**Motivo**: validar primeiro o conceito central "orçamento → destinos" sem complicar a experiência de entrada. Análise de calendário completo (ex.: "qualquer dia entre 1 e 30 de outubro", o Voa Radar encontrando os melhores dias) fica para a v0.3, onde pode virar uma das experiências mais fortes do produto — não uma feature secundária espremida na v0.2.
