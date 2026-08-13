# Voa Radar v0.3 — Plano de Implementação

## Regra

Implementar em fases. Nunca executar tudo de uma vez.

## FASE 0 — Baseline

Antes de qualquer alteração: ler documentação, executar testes, verificar Git, confirmar `v0.2.0`, confirmar working tree limpo.

## FASE 1 — Modelo de dados

Projetar entities, relationships, migrations, indexes. Não implementar até aprovação.

## FASE 2 — PostgreSQL (Supabase)

Configurar conexão, environment, migration, inicialização. Nunca armazenar secrets no código.

## FASE 3 — Repository

Implementar persistência. Testar CRUD necessário.

## FASE 4 — Historical Data

Implementar armazenamento das observações. `MockFlightProvider` alimenta o banco.

## FASE 5 — Analytics Engine

Implementar mean, median, min, max, variation, score, confidence. Testar extensivamente.

## FASE 6 — Price Intelligence Service

Combinar Repository + Analytics Engine.

## FASE 7 — API

Criar endpoint de análise (ex.: `GET /flights/price-intelligence/{offer_id}`, adaptado ao padrão de rotas já usado no projeto — sem prefixo `/api/v1/`, ver [ARCHITECTURE.md](ARCHITECTURE.md) da v0.1). Resposta normalizada.

## FASE 8 — Frontend

Criar Price Intelligence Card, Analysis View, gráfico, score, confiança, explicação.

## FASE 9 — Integração

Conectar frontend ao backend.

## FASE 10 — Testes

`pytest`, Vitest, Playwright. Casos: poucos dados, preço mínimo, preço máximo, preço médio, outliers, moedas, rota diferente, datas diferentes.

## FASE 11 — Auditoria

Regressão v0.2, responsividade, console, network, performance, segurança, migrations, secrets.

## FASE 12 — Documentação

Atualizar README, PROJECT_CONTEXT, ROADMAP, DECISIONS.

## FASE 13 — Release

Somente após aprovação: commit, tag `v0.3.0`, push.
