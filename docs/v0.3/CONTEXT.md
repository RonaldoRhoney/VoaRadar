# Voa Radar v0.3 — Contexto

## 1. Estado anterior

A v0.1 estabeleceu a fundação técnica. A v0.2 estabeleceu a experiência de exploração de destinos.

A v0.2 permite ao usuário responder: **"Para onde posso viajar com meu orçamento?"**

A v0.3 deverá responder: **"Esse preço é realmente uma boa oportunidade?"**

## 2. Objetivo

Transformar o Voa Radar de um mecanismo de descoberta em uma plataforma capaz de analisar preços.

## 3. Conceito

O sistema deverá comparar uma oferta atual com o histórico disponível para aquela rota e contexto de viagem.

Exemplo:

```text
BEL → REC
Preço atual: R$ 429

Histórico:
Mínimo: R$ 399
Médio:  R$ 620
Máximo: R$ 890

Resultado: 🟢 Boa oportunidade
```

## 4. Importante

O sistema NÃO deve afirmar que um preço é barato em termos absolutos sem possuir dados suficientes. O indicador deve ser baseado no histórico disponível.

## 5. Dados

Nesta versão inicial, os dados poderão continuar sendo gerados pelo ambiente controlado do projeto (`MockFlightProvider`). A arquitetura deve permitir futuramente substituir o provider por dados reais, sem reescrever o motor de análise.

## 6. Objetivo técnico

Introduzir: PostgreSQL (via Supabase — ver [DECISIONS.md](DECISIONS.md) DEC-013), persistência, histórico, agregações, análise, score, API de inteligência, visualização de histórico.

## 7. Objetivo de produto

O usuário deverá conseguir compreender rapidamente: preço atual, preço médio, menor preço observado, maior preço observado, variação, classificação da oportunidade.

## 8. Princípio

Nunca fabricar confiança. Se houver poucos dados: "Ainda temos poucos dados para avaliar esta oportunidade." — nunca "Excelente oportunidade" sem base.

## 9. Visão futura

A inteligência criada nesta versão serve de base para v0.4 (alertas) e v0.5 (recomendações).
