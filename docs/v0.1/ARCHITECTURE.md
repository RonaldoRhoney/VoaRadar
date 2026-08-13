# Voa Radar v0.1 — Arquitetura

> Documento retrospectivo — descreve a arquitetura como ela estava na tag `v0.1.0`, antes da evolução da v0.2 (que trocou `/flights/budget-search` por `/flights/explore` e introduziu a separação Destino/Oferta). Ver [../v0.2/ARCHITECTURE.md](../v0.2/ARCHITECTURE.md) para o estado atual.

## 1. Backend

FastAPI, estrutura modular:

```
backend/
└── app/
    ├── api/         # rotas (health, flights)
    ├── core/         # config (pydantic-settings)
    ├── schemas/      # BudgetSearchRequest, BudgetDestination
    ├── services/      # BudgetSearchService
    ├── providers/     # FlightProvider (abstrato), MockFlightProvider
    └── main.py
```

`requirements/base.txt` (runtime) + `requirements/dev.txt` (+ testes), no lugar de um `requirements.txt` único.

## 2. Provider

`FlightProvider` abstrato, com um único método `get_budget_destinations(origin_city, month, budget) -> list[BudgetDestination]`. `MockFlightProvider` como única implementação — um destino, um preço (a separação Destino/Oferta só chega na v0.2).

## 3. Service

`BudgetSearchService`: recebe o provider por injeção (default `MockFlightProvider`), aplica ordenação por preço.

## 4. API

```
POST /flights/budget-search

Request:  { budget, origin_city, month, flexible }
Response: BudgetDestination[]  (array plano — sem "search"/"metadata")
```

`GET /health` — health check simples.

## 5. Frontend

```
frontend/src/
├── components/    # Header, Footer, Layout
├── pages/          # Home, Results, NotFound
├── features/
│   └── budget-search/   # BudgetSearchForm, useBudgetSearch
├── services/       # api.ts (fetch + tratamento de erro)
├── types/          # flight.ts
├── utils/          # format.ts
└── tests/e2e/       # Playwright
```

## 6. Banco de dados

Nenhum — dados mock vivem em memória, dentro do próprio `MockFlightProvider`.

## 7. Segurança

Variáveis de ambiente (`.env.example` sem segredo), validação de entrada (`budget > 0`), sem API key nenhuma no código (nada a esconder ainda, sem provedor real integrado).

## 8. Testabilidade

5 testes `pytest` (health, dentro do orçamento, lista vazia, validação, service com provider injetado), 3 testes Vitest (formatação, hook de busca), 1 E2E Playwright (fluxo completo).
