# Voa Radar v0.1 — Critérios de Aceite

> Documento retrospectivo, no formato usado a partir da v0.2. Detalhe completo em [../AUDIT_V0.1.md](../AUDIT_V0.1.md).

## Busca

- [x] Usuário informa orçamento.
- [x] Usuário informa origem.
- [x] Usuário escolhe período (mês).
- [x] Usuário pode selecionar "Não sei para onde ir".

## Resultados

- [x] Sistema retorna destinos dentro do orçamento.
- [x] Resultados ordenados por preço.
- [x] Detalhe da oportunidade (rota + preço) ao clicar.

## UX

- [x] Loading (skeleton).
- [x] Empty state (mensagem própria, não "nenhum resultado" cru).
- [x] Error state (testado contra o backend real derrubado).
- [x] Mobile (390px).
- [x] Desktop (1280px).
- [x] Página "não encontrada" (404 do frontend).

## Backend

- [x] Endpoint funcionando (`POST /flights/budget-search`).
- [x] Schemas validados (`budget > 0`).
- [x] Provider funcionando (`MockFlightProvider` atrás de `FlightProvider`).
- [x] Erros tratados.

## Testes

- [x] Pytest (5).
- [x] Vitest (3).
- [x] Playwright (1).

## Qualidade

- [x] Sem erros no console.
- [x] Sem dados mock apresentados como reais.
- [x] Sem secrets no código.
- [x] Sem código morto relevante (resíduo do scaffold do Vite removido na auditoria).

## Documentação

- [x] PRD, PROJECT_CONTEXT, ROADMAP.
- [x] Diário de decisões (`DECISIONS.md`).
- [x] Auditoria completa (`AUDIT_V0.1.md`).

## Git

- [x] Commit.
- [x] Tag `v0.1.0`.
- [x] Push.
