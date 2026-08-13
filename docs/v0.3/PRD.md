# Voa Radar v0.3 — PRD

## 1. Nome

Voa Radar — Price Intelligence

## 2. Objetivo principal

Adicionar inteligência de preços às ofertas encontradas pelo Voa Radar.

## 3. Funcionalidades

### 3.1 Histórico

Registrar preços observados. Cada registro deverá conter, quando disponível: rota, origem, destino, data de viagem, data de retorno, companhia, preço, moeda, quantidade de escalas, duração, momento da coleta.

### 3.2 Preço atual

Toda oferta poderá possuir preço atual e momento da coleta.

### 3.3 Estatísticas

Para cada contexto analisável: preço mínimo, preço médio, preço máximo, mediana, quantidade de observações. A mediana deve ser usada quando apropriado para reduzir influência de outliers.

### 3.4 Comparação

Calcular percentual abaixo/acima da média. Exemplo: atual R$ 429, média R$ 620 → -30,8%.

### 3.5 Score

Criar `opportunity_score`, escala 0–100, considerando somente dados disponíveis.

### 3.6 Classificação

80–100 EXCELLENT · 60–79 GOOD · 40–59 NORMAL · 20–39 EXPENSIVE · 0–19 VERY_EXPENSIVE. Limites configuráveis.

### 3.7 Confiança

Criar `confidence_level`: LOW / MEDIUM / HIGH, dependendo principalmente da quantidade e qualidade dos dados.

### 3.8 Regra de dados insuficientes

Sem observações suficientes, não apresentar classificação forte: "Ainda estamos coletando dados para avaliar este preço."

### 3.9 Melhor data

Quando houver dados suficientes: menor preço, melhor data, diferença para outras datas.

### 3.10 Calendário (arquitetura preparada, não implementado visualmente ainda)

```
01/10 — R$ 620
05/10 — R$ 580
10/10 — R$ 429  ⭐ Melhor data encontrada
15/10 — R$ 517
```

### 3.11 Gráfico

Histórico de preços — eixo X data da observação, eixo Y preço.

### 3.12 Comparação com orçamento

"✓ Dentro do orçamento" é diferente de "Boa oportunidade" — não confundir os dois conceitos na UI.

### 3.13 Comparação conceitual

O sistema diferencia: **Orçamento** (o que o usuário pode pagar), **Preço** (quanto custa a oferta), **Oportunidade** (como esse preço se comporta em relação ao histórico).

## 4. Fora da v0.3

Alertas, notificações, IA generativa, previsão futura de preços, recomendação automática de compra, booking, pagamento, afiliados, login obrigatório, scraping, integração obrigatória com companhia aérea.

## 5. Dados reais

A arquitetura deve estar preparada para receber dados reais futuramente. Nenhum dado mock deve ser apresentado como real.

## 6. Resultado esperado

O usuário deve conseguir olhar uma oferta e entender "quanto custa?" e também "esse preço parece bom comparado ao que o Voa Radar já observou?"
