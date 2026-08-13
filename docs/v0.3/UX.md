# Voa Radar v0.3 — UX

## 1. Objetivo

Transformar dados de preço em informação simples.

## 2. Card de oportunidade

```text
✈️ Recife
BEL → REC
R$ 429
🟢 Boa oportunidade

Preço médio: R$ 620
Você está pagando aproximadamente 31% abaixo da média.

[Ver análise]
```

## 3. Estado com poucos dados

Não mostrar "🟢 Excelente oportunidade". Mostrar: "📊 Ainda estamos aprendendo esta rota. Dados disponíveis: 8 observações".

## 4. Tela de análise

Título "Análise de preço": preço atual, preço médio, menor preço observado, maior preço observado, score (ex.: 82/100 — Boa oportunidade).

## 5. Gráfico

Histórico de preços, tooltip mostrando data e preço.

## 6. Explicação

Nunca mostrar só números: "O preço atual está 31% abaixo da média observada para este contexto."

## 7. Confiança

🟢 Alta confiança / 🟡 Confiança moderada / ⚪ Poucos dados.

## 8. Mobile

Prioridade: preço → classificação → média → score → gráfico → detalhes.

## 9. Transparência

Sempre indicar: "Análise baseada no histórico disponível pelo Voa Radar." Nunca: "Melhor preço do mercado."

## 10. Linguagem

Simples. Evitar "desvio padrão", "percentil", "z-score" na interface principal — esses conceitos podem existir em detalhes técnicos, não na experiência principal.
