# Voa Radar v0.3 — Arquitetura

## 1. Evolução

```
v0.2:  Provider → Service → API → Frontend
v0.3:  Provider → Collector → Persistence → Analytics → API → Frontend
```

## 2. Backend

Mantém FastAPI. Estrutura:

```
backend/
└── app/
    ├── api/
    ├── core/
    ├── schemas/
    ├── services/
    ├── providers/
    ├── models/          # novo — entidades de banco
    ├── repositories/     # novo — persistência
    ├── analytics/        # novo — motor de análise
    └── main.py
```

## 3. Models

PostgreSQL (via Supabase) passa a fazer parte da arquitetura. Modelos só serão criados após aprovação do modelo de dados ([DATA_MODEL.md](DATA_MODEL.md)).

## 4. Repository

Responsável por persistência — ex.: `PriceHistoryRepository`. SQL não fica direto nos endpoints.

## 5. Analytics

Módulo separado. Responsabilidades: média, mediana, mínimo, máximo, variação, score, confiança.

## 6. Provider

Continua `FlightProvider` / `MockFlightProvider`. Futuramente, `RealFlightProvider`.

## 7. Collector

Responsável por receber ofertas do provider e armazenar observações. Não mistura coleta com análise.

## 8. Fluxo

```
Provider → Normalized Offers → Collector → Database → Analytics Engine → Price Intelligence API → Frontend
```

## 9. Frontend

Nova feature: `features/price-intelligence/` — análise, score, histórico, gráfico, confiança.

## 10. Princípio

Analytics não depende do frontend. O backend calcula, o frontend apresenta.

## 11. Testabilidade

O motor de análise recebe dados e retorna resultados determinísticos — não depende diretamente do banco para os cálculos unitários.

## 12. Preparação para dados reais

Nenhum componente deve assumir que o provider é mock. O contrato normalizado permanece independente do fornecedor.
