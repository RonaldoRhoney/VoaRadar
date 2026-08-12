# PRD — Voa Radar

## Problema

Buscar passagem aérea hoje exige já saber origem, destino e data. Quem só sabe "quero viajar, tenho R$ X" não é bem atendido pelos buscadores tradicionais.

## Proposta

Um buscador que parte do orçamento: o usuário informa quanto quer gastar, de onde sai e quando, e recebe destinos que cabem nesse valor — podendo então aprofundar numa oportunidade específica.

## Escopo do MVP

1. **Tela principal (prioridade #1)** — formulário: orçamento (slider), origem (cidade), mês de viagem, checkbox "Não sei para onde ir".
2. **Resultados por orçamento** — lista de destinos dentro do valor informado, ordenados do mais barato ao mais caro.
3. **Detalhe da oportunidade** — preço e rota ao clicar em "Ver oportunidade".
4. Rodapé e identidade visual padrão RhoneyInc.

Status: itens 1–4 implementados com dados mock (frontend e backend). Ver [ROADMAP.md](ROADMAP.md).

## Explicitamente fora do MVP

- Busca tradicional origem/destino/data como fluxo principal.
- Reserva e pagamento.
- Contas de usuário, buscas salvas, alertas de preço.
- Itinerários multi-trecho.
- Integração com fonte real de dados de voo (Amadeus ou equivalente).

Esses itens só entram quando explicitamente decididos — ver regra de "sugestão futura" em [CLAUDE.md](CLAUDE.md).

## Critério de sucesso do MVP

Um usuário consegue, sem sair da tela inicial, dizer quanto quer gastar e receber destinos plausíveis dentro do orçamento — mesmo que os dados ainda sejam de exemplo.
