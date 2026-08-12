# Voa Radar v0.2 — Implementação

Este documento é o roteiro de execução — particularmente importante para o Claude Code seguir.

## Regra principal

Implementar em pequenas etapas. Não executar todo o documento de uma vez.

## FASE 1 — Análise

Antes de alterar: ler documentação, analisar código v0.1, verificar testes, verificar arquitetura, identificar regressões. **Não modificar código.**

## FASE 2 — Contrato da API

Definir request, response, schemas, validações. Testar.

## FASE 3 — Mock Provider

Expandir `MockFlightProvider` para retornar múltiplos destinos. Testar.

## FASE 4 — Service

Implementar serviço de exploração. Responsabilidades: receber parâmetros, consultar provider, filtrar, ordenar, classificar. Testar.

## FASE 5 — Endpoint

Conectar service ao FastAPI. Testar: sucesso, parâmetros inválidos, vazio, erro.

## FASE 6 — Frontend

Implementar: formulário, filtros, resultados, cards, ordenação, estados.

## FASE 7 — Integração

Frontend deve consumir backend. Não duplicar lógica de negócio no frontend.

## FASE 8 — UX

Validar: mobile, desktop, loading, vazio, erro, acessibilidade.

## FASE 9 — Testes

Executar: pytest, Vitest, Playwright. Corrigir regressões.

## FASE 10 — Auditoria

Verificar: console, network, erros, responsividade, performance, código morto, dependências.

## FASE 11 — Documentação

Atualizar: README, roadmap, decisões, documentação v0.2.

## FASE 12 — Commit

Somente após aprovação:

```
git status
git add .
git commit -m "feat: implement Voa Radar v0.2 explore"
git tag v0.2.0
```

## Regra

Depois de cada fase, informar: **Implementado / Testado / Pendente / Riscos / Próximo passo**.

Não avançar automaticamente quando houver decisão de produto.
