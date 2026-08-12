# Voa Radar v0.2 — Critérios de Aceite

A v0.2 somente será considerada concluída quando:

## Busca

- [x] Usuário informa orçamento.
- [x] Usuário informa origem.
- [x] Usuário escolhe período. (mês + flexibilidade — ver DEC-008 em [DECISIONS.md](DECISIONS.md))
- [x] Usuário informa passageiros.
- [x] Usuário pode selecionar "Não sei para onde ir".

## Exploração

- [x] Sistema retorna múltiplos destinos.
- [x] Resultados respeitam orçamento.
- [x] Resultados possuem preço.
- [x] Resultados possuem data.
- [x] Resultados possuem duração.
- [x] Resultados possuem escalas.
- [x] Resultados possuem companhia.

## Ordenação

- [x] Menor preço.
- [x] Melhor oportunidade. (mesmo critério de menor preço — ver DEC-005-B em [DECISIONS.md](DECISIONS.md), não fabricamos um índice de oportunidade)
- [x] Menor duração.
- [x] Menos escalas.

## Filtros

- [x] Preço.
- [~] Escalas. (toggle "somente voos diretos" — não distingue "1 escala" separadamente, ver DEC-010)
- [x] Duração.
- [ ] Período. (não implementado — período já é definido na própria busca; ver DEC-009)

## UX

- [x] Loading.
- [x] Empty state. (com sugestão de `near_budget`, PRD 3.11/3.12)
- [x] Error state.
- [x] Mobile. (390px, validado)
- [x] Tablet. (768px, validado)
- [x] Desktop. (1280px, validado)
- [~] Acessibilidade básica. (labels em todos os campos, `role="alert"`/`aria-live` nos estados, foco visível padrão do navegador preservado — sem auditoria completa de navegação por teclado/leitor de tela)

## Backend

- [x] Endpoint funcionando. (`POST /flights/explore`)
- [x] Schemas validados.
- [x] Provider funcionando. (`MockFlightProvider`, múltiplas ofertas por destino)
- [x] Service testado. (`ExploreService`, testes unitários sem `TestClient`)
- [x] Erros tratados.

## Testes

- [x] Pytest. (10/10)
- [x] Vitest. (13/13)
- [x] Playwright. (2/2)

## Qualidade

- [x] Sem erros no console. (verificado via asserção no E2E e capturas manuais)
- [x] Sem chamadas duplicadas desnecessárias. (uma chamada por busca, com cancelamento em unmount)
- [x] Sem dados mock apresentados como reais. ("dados de exemplo (mock)" visível em toda tela de resultado)
- [x] Sem secrets no código.
- [x] Sem regressão da v0.1. (suíte inteira migrada e verde, nenhum comportamento válido perdido)

## Documentação

- [x] PRD atualizado. (desvios registrados em DECISIONS, não no PRD original — é o documento de intenção, não de status)
- [x] README atualizado.
- [x] Decisions atualizado.
- [x] Roadmap atualizado.

## Git

- [x] Commit.
- [x] Tag `v0.2.0`.
- [x] Push.
