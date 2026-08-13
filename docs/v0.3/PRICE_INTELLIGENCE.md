# Voa Radar — Price Intelligence Engine

> O documento mais importante da v0.3.

## 1. Objetivo

Transformar observações históricas em indicadores compreensíveis.

## 2. Dados de entrada

O motor recebe: `current_price`, `historical_prices`, `sample_size`. Contexto: `route`, `departure_date`, `return_date`, `passengers`, `currency`.

## 3. Estatísticas

`minimum`, `maximum`, `mean`, `median`.

## 4. Variação

```
percentage_vs_mean = (current_price - mean) / mean * 100
```

## 5. Distância do mínimo

```
percentage_vs_min = (current_price - minimum) / minimum * 100
```

## 6. Score

Baseado principalmente na posição relativa do preço atual dentro da distribuição histórica. Não criar fórmula artificialmente complexa. Primeira versão: quanto menor o preço relativo ao histórico, maior o score.

## 7. Confiança

Considera `sample_size`. Sugestão inicial: <10 → LOW, 10–29 → MEDIUM, ≥30 → HIGH. Valores configuráveis.

## 8. Classificação

80–100 EXCELLENT · 60–79 GOOD · 40–59 NORMAL · 20–39 EXPENSIVE · 0–19 VERY_EXPENSIVE.

## 9. Regra de segurança

O score não representa probabilidade de o preço cair. Nunca afirmar "compre agora" ou "o preço vai subir" — não prever o futuro.

## 10. Linguagem

Dizer "o preço está abaixo da média observada". Nunca "esse é o menor preço que você encontrará".

## 11. Dados insuficientes

`sample_size` baixo → `confidence = LOW` e a interface informa "ainda temos poucos dados para avaliar esta oportunidade".

## 12. Determinismo

Mesmos dados de entrada → resultado idêntico. Facilita testes.

## 13. Configuração

Limites de score e confiança centralizados — não espalhar números mágicos pelo código.

## 14. Futuro (não implementar na v0.3)

Percentis, sazonalidade, antecedência, comparação entre períodos, modelos estatísticos, machine learning.
