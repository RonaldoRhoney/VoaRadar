# Voa Radar v0.2 — PRD

## 1. Nome

Voa Radar — Explore

## 2. Objetivo

Criar uma experiência de exploração de destinos baseada no orçamento do usuário.

## 3. Funcionalidades

### 3.1 Origem

O usuário poderá informar cidade, aeroporto ou código IATA. A interface deve permitir pesquisa por nome.

Exemplo: "Belém" deve apresentar "Belém — Val-de-Cans — BEL". O usuário não precisa conhecer o código IATA.

### 3.2 Orçamento

O usuário informa seu orçamento (ex.: R$ 800). O campo deve: aceitar somente valores válidos, formatar moeda, impedir valores negativos, fornecer feedback visual.

### 3.3 Período

Permitir: mês específico, intervalo, datas flexíveis. Na primeira implementação da v0.2, priorizar **mês + flexibilidade** (ver nota em `DECISIONS.md` sobre simplificação de período).

### 3.4 Passageiros

Permitir inicialmente: adultos. Preparar arquitetura para crianças e bebês. Não implementar regras complexas de tarifa ainda.

### 3.5 Modo Explore

O usuário poderá selecionar "Não sei para onde ir". Quando selecionado: destino deixa de ser obrigatório, sistema busca destinos compatíveis, resultados são organizados por oportunidade.

### 3.6 Resultados

Cada destino deve apresentar: destino, cidade, aeroporto, preço, data, duração, escalas, companhia, indicador de oportunidade, botão de detalhes.

### 3.7 Ordenação

Permitir ordenar por: menor preço, melhor oportunidade, menor duração, menos escalas.

### 3.8 Filtros

Filtros iniciais: preço máximo, sem escalas, uma escala, duração, período. Os filtros devem aparecer de maneira simples. No mobile, utilizar painel ou bottom sheet.

### 3.9 Cards

Cada oportunidade deve possuir um card visualmente claro. Exemplo:

```
✈️ Recife
REC
A partir de
R$ 429
🟢 Boa oportunidade
📅 14–18 Outubro
⏱ 4h20
1 escala
[Ver oportunidade]
```

### 3.10 Detalhes

Ao abrir uma oportunidade, mostrar: origem, destino, datas, preço, companhia, duração, escalas, horário, observações, origem do dado. O botão principal deve permitir futuramente direcionar para o fornecedor — na v0.2 poderá utilizar link mockado.

### 3.11 Nenhum resultado

Nunca mostrar apenas "Nenhum resultado". Exemplo:

> Não encontramos oportunidades até R$ 500.
>
> Encontramos opções a partir de R$ 537.
>
> [Ver opções]

Também sugerir: aumentar orçamento, ampliar período, aceitar escala.

### 3.12 Resultado acima do orçamento

Se uma oportunidade estiver acima do orçamento, ela poderá aparecer somente se o usuário ativar "Mostrar opções próximas ao orçamento".

Exemplo: orçamento R$ 500, resultado R$ 537 → mostrar "Apenas R$ 37 acima do seu orçamento."

### 3.13 Responsividade

A experiência deve funcionar em smartphone, tablet e desktop. Mobile-first.

### 3.14 Performance

Evitar: componentes desnecessários, chamadas duplicadas, renders excessivos, dependências desnecessárias.

## 4. Fora da v0.2

Não implementar: API real, scraping, login, pagamentos, alertas, IA, notificações, histórico permanente, sistema de afiliados, Android.

## 5. Resultado esperado

Usuário entra, informa (R$ 800, Belém, Outubro, "Não sei para onde ir"), clica "Encontrar viagens" e recebe uma experiência convincente de descoberta de destinos.
