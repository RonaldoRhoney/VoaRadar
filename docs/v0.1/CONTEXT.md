# Voa Radar v0.1 — Contexto

> Documento retrospectivo — v0.1 já está concluída (tag `v0.1.0`). Escrito depois, no mesmo formato usado para planejar a v0.2, pra manter o histórico do projeto consistente. Contexto de produto completo (que transcende qualquer versão) em [../../PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md).

## 1. Objetivo

Construir a fundação técnica e visual do Voa Radar: primeira versão navegável da experiência central do produto, com arquitetura já preparada para evoluir (múltiplos provedores de voo, múltiplas versões), mesmo usando dados mock do início ao fim.

## 2. A ideia validada nesta versão

> "Tenho X reais. Para onde posso viajar?"

Diferente do buscador tradicional (origem → destino → data), a v0.1 já nasceu **orçamento-primeiro**: o usuário diz quanto quer gastar, de onde sai e quando, e recebe destinos que cabem nesse valor.

## 3. Usuário

Pessoas planejando viagem que querem comparar preços rapidamente — incluindo quem ainda não decidiu o destino, só sabe quanto quer gastar.

## 4. Exemplo

```text
Orçamento: R$ 800
Origem: Belém
Período: Outubro

Resultado:
Recife       R$ 429
Fortaleza    R$ 517
Brasília     R$ 598
Salvador     R$ 689
```

## 5. Dados mock

Preços e destinos são fictícios, claramente identificados no código (`MOCK DATA`, `MockFlightProvider`) e na interface ("dados de exemplo (mock)"). Nenhuma integração com fonte real de dados de voo nesta versão.

## 6. O que ficou de fora, por decisão

Busca tradicional origem/destino/data como fluxo principal, reserva e pagamento, contas de usuário, buscas salvas, alertas de preço, itinerários multi-trecho, integração real de dados de voo. Ver [PRD.md](PRD.md).

## 7. Visão futura (no momento da v0.1)

- **v0.2** — Explorar destinos (múltiplas ofertas por destino, filtros, ordenação).
- **v0.3** — Histórico e análise de preços.
- **v0.4** — Alertas.
- **v0.5** — Inteligência (IA).
- **v1.0** — Plataforma pública.

## 8. Marca

- Produto: Voa Radar
- Empresa: RhoneyInc
- Posicionamento: "Seu radar para viajar pagando menos."
