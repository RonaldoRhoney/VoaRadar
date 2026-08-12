# Voa Radar v0.2 — Contexto

## 1. Objetivo

A versão 0.1 do Voa Radar foi concluída, implementada e auditada.

A v0.1 estabeleceu a fundação técnica e visual do produto:

- frontend React + TypeScript + Vite;
- Tailwind CSS;
- backend FastAPI;
- comunicação frontend/backend;
- arquitetura modular;
- `FlightProvider`;
- `MockFlightProvider`;
- testes;
- tratamento de estados;
- experiência inicial de busca;
- documentação;
- estrutura preparada para evolução.

A v0.2 NÃO deve reconstruir a v0.1. Ela deve evoluir a fundação existente.

## 2. Objetivo da v0.2

O objetivo principal é implementar a experiência de:

> "Tenho determinado orçamento. Para onde posso viajar?"

A aplicação deverá permitir que o usuário explore destinos compatíveis com:

- origem;
- orçamento;
- período;
- flexibilidade de datas;
- número de passageiros.

## 3. Mudança conceitual

Na v0.1 o fluxo principal é:

Origem → orçamento → período → resultados.

Na v0.2 o conceito passa a ser:

Orçamento → possibilidades → destinos → comparação → oportunidade.

O orçamento continua sendo o principal ponto de partida.

## 4. Usuário

O usuário pode não saber o destino. Ele pode simplesmente pensar:

> "Tenho R$ 700 e quero viajar."

O Voa Radar deve transformar essa intenção em possibilidades concretas.

## 5. Exemplo

Entrada:

- Origem: Belém
- Orçamento: R$ 800
- Período: Outubro
- Flexibilidade: Qualquer data do mês
- Passageiros: 1 adulto

Resultado:

- Recife — R$ 429
- Fortaleza — R$ 517
- Brasília — R$ 598
- Salvador — R$ 689

## 6. Importante

Os preços continuam sendo MOCK DATA nesta versão enquanto não houver integração com um provedor real validado. Nunca apresentar mock como preço real.

## 7. Visão futura

A v0.2 prepara o produto para:

- v0.3 → histórico e análise
- v0.4 → alertas
- v0.5 → inteligência
- v1.0 → plataforma pública

O código da v0.2 deve facilitar essas evoluções.

## 8. Princípio

Não adicionar funcionalidades apenas porque são tecnicamente interessantes. Toda implementação deve melhorar a experiência:

> "Quanto posso gastar e para onde consigo viajar?"

## 9. Marca

- Produto: Voa Radar
- Empresa: RhoneyInc
- Slogan: "Voa Radar — seu radar para viajar pagando menos."
