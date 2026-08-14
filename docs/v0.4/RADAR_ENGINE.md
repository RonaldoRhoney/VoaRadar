# Voa Radar v0.4 — Radar Engine

## 1. Responsabilidade

Decidir, de forma pura e determinística, se um Radar deve disparar diante de um novo preço observado. Não lê banco, não grava nada, não sabe de cooldown (isso é responsabilidade do `RadarEvaluationService`, não do engine — mesma separação que `analytics/engine.py` mantém em relação a `PriceIntelligenceService` na v0.3).

## 2. Contrato

```python
def evaluate_radar(radar: RadarConfig, current_price: float, intelligence: PriceIntelligence) -> bool:
    """True se a condição do Radar foi satisfeita por este preço/análise."""
```

- `condition_type == "PRICE_BELOW"` → `current_price < radar.condition_price`.
- `condition_type == "OPPORTUNITY_CLASSIFICATION"` → `intelligence.classification == radar.condition_classification`.

Sem efeitos colaterais, sem exceção esperada em caminho normal — mesmo padrão de testabilidade que o analytics engine da v0.3 já validou (14 testes puros).

## 3. Fluxo de disparo (orientado a evento)

```
Nova PriceSnapshot persistida (record_observation, v0.3)
        ↓
RadarEvaluationService.evaluate_for_route(route_id, new_price)
        ↓
Busca Radares ACTIVE com (origin, destination) = rota da snapshot
        ↓
Para cada Radar:
   PriceIntelligenceService.analyze_route(...)  (reaproveitado da v0.3)
        ↓
   radar_engine.evaluate_radar(...)
        ↓
   Disparou? → aplica cooldown (ALERT_RULES.md) → grava radar_event (+ notification se passar do cooldown)
```

**Risco registrado explicitamente** (já sinalizado na análise arquitetural aprovada): este fluxo só é acionado quando `record_observation` é chamado. Hoje isso acontece via `scripts/seed_history.py` (coleta simulada). Quando a integração real de provedor chegar (v0.5+), a avaliação de Radar só continua funcionando se a nova coleta também passar por esse mesmo ponto — precisa virar teste de integração explícito ("toda gravação de snapshot aciona avaliação de radar"), não uma suposição implícita.

## 4. Por que não um worker/scheduler

Registrado como decisão consciente, não lacuna: ver `DECISIONS.md` DEC-104. Resumo — não há hoje coleta automática contínua de preços reais; um scheduler não teria o que verificar de forma independente da própria coleta. Introduzir infraestrutura de agendamento antes de ter o que agendar seria complexidade sem função.

## 5. Testabilidade

`evaluate_radar` testável com dados sintéticos, sem banco, sem rede — mesmo padrão de testes unitários puros já estabelecido pro `analytics/engine.py`. `RadarEvaluationService` (a orquestração) testável contra SQLite em memória, mesmo padrão de `PriceIntelligenceService`/`repositories` da v0.3.
