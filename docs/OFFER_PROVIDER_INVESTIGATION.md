# Investigação real: provider de oferta real (2026-08-17)

> Complementa `docs/DATA_SOURCES.md`/`API_LIMITS.md` (DEC-117) — aquela investigação cobriu Open Finance-adjacent/dados de referência; esta cobre especificamente oferta comprável (preço + reserva) em tempo real, o que substituiria o `MockFlightProvider`.

## O que foi verificado (WebSearch + WebFetch, 2026-08-17)

- **Duffel**: acesso técnico à API é livre (`sign up`, chave de teste `duffel_test_...`, saldo ilimitado simulado). Mas o modo de teste só garante comportamento previsível com a companhia fictícia própria da Duffel ("Duffel Airways") — a própria documentação deles admite que não há preço/horário realista nesse modo; usar companhias reais em modo de teste depende do sandbox de cada companhia, sem garantia. Em produção: US$3 por pedido confirmado, mais US$0,005 por busca acima de uma cota de 1.500 buscas grátis **por reserva confirmada no mês** — ou seja, sem nenhuma reserva real acontecendo (que é o estado atual do VoaRadar — "Ir para o fornecedor" ainda desabilitado), a cota de busca grátis é efetivamente zero.
- **Kiwi.com (Tequila API)**: não aceita mais cadastro self-service — programa fechado, só parceiro convidado, com exigência informada de 50.000 usuários ativos/mês pra acesso via revenda (Travelpayouts). Inacessível a um produto novo, independente de orçamento.
- **Amadeus Self-Service**: confirmado descontinuado em 17/jul/2026 (achado anterior, DEC-117 em `docs/v0.4/DECISIONS.md`).

## Conclusão

Mesma conclusão estrutural do Open Finance (DEC-011/012 do FinTra, por analogia): **não existe caminho zero-custo real pra oferta de voo comprável hoje**, nem para um produto em estágio inicial sem volume de reserva. As opções restantes são:

1. Contratar um plano pago de algum provider (Duffel produção, ou renegociar acesso à Kiwi caso o volume de usuário cresça) — decisão de orçamento do usuário.
2. Continuar com `MockFlightProvider`, dado sempre identificado como exemplo (já é a prática atual, `CLAUDE.md` §7/§16) — sem prazo definido pra sair do mock.

## Status

`FlightProvider` já é uma interface abstrata (`app/providers/base.py`) desde o V0.1 — trocar `MockFlightProvider` por um provider real é uma implementação isolada quando/se a decisão de orçamento for tomada, sem precisar redesenhar nada. Nenhum código de integração real foi escrito — só esta investigação.
