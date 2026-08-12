# Voa Radar v0.2 — Arquitetura

## 1. Regra

A arquitetura da v0.1 deve ser preservada. A v0.2 deve evoluir, não reconstruir.

## 2. Backend

FastAPI. Estrutura esperada (já existente desde a v0.1):

```
backend/
└── app/
    ├── api/
    ├── core/
    ├── schemas/
    ├── services/
    ├── providers/
    └── main.py
```

## 3. Provider

Manter `FlightProvider`. Implementação: `MockFlightProvider`. Não criar API real nesta versão.

## 4. Service

A lógica de exploração deve ficar em service — ex.: `BudgetSearchService` (ou sua evolução). Responsabilidades: validar orçamento, consultar provider, normalizar resultados, filtrar, ordenar, classificar.

## 5. API

Criar/evoluir endpoint de exploração. Exemplo conceitual:

```
GET/POST /api/v1/explore

Request:  origin, budget, period, passengers, flexible_dates
Response: destinations, offers, metadata
```

## 6. Response

A resposta não deve expor detalhes internos do provider. O frontend deve receber um modelo normalizado.

## 7. Frontend

Manter a feature `features/budget-search/`. Se a exploração justificar separação, criar `features/explore/`. Não criar abstrações genéricas antecipadamente.

## 8. Estado

O estado da busca deve permanecer controlado pela feature. Evitar estado global sem necessidade.

## 9. Mock

`MockFlightProvider` deverá simular: múltiplos destinos, preços diferentes, datas, escalas, duração, companhia. Os dados devem parecer realistas, mas permanecer claramente fictícios.

## 10. Futuro

A arquitetura deverá permitir:

```
FlightProvider
    ↓
MockFlightProvider
```

e, posteriormente:

```
FlightProvider
    ↓
RealProvider
```

sem reescrever o frontend.

## 11. Banco

Não implementar PostgreSQL definitivo apenas para a v0.2. Dados continuam temporários.

## 12. Segurança

Manter: environment variables, validação, rate limiting quando aplicável, tratamento de erros, logs.

## 13. Testabilidade

A lógica de filtro, ordenação, classificação e orçamento deve ser testável independentemente da interface.
