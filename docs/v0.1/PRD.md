# Voa Radar v0.1 — PRD

> Documento retrospectivo — mesmo escopo do [../../PRD.md](../../PRD.md) original, reorganizado no formato usado a partir da v0.2 para manter os dois no mesmo padrão.

## 1. Nome

Voa Radar — Fundação

## 2. Objetivo

Um buscador que parte do orçamento: o usuário informa quanto quer gastar, de onde sai e quando, e recebe destinos que cabem nesse valor — podendo então aprofundar numa oportunidade específica.

## 3. Problema

Buscar passagem aérea hoje exige já saber origem, destino e data. Quem só sabe "quero viajar, tenho R$ X" não é bem atendido pelos buscadores tradicionais.

## 4. Funcionalidades

### 4.1 Tela principal (prioridade #1)

Formulário: orçamento (slider), origem (cidade, texto livre), mês de viagem, checkbox "Não sei para onde ir".

### 4.2 Resultados por orçamento

Lista de destinos dentro do valor informado, ordenados do mais barato ao mais caro. Um preço por destino (a distinção Destino/Oferta só chega na v0.2).

### 4.3 Detalhe da oportunidade

Preço e rota ao clicar em "Ver oportunidade".

### 4.4 Identidade visual

Rodapé e identidade visual padrão RhoneyInc (skill `footer-padrao`).

## 5. Fora da v0.1

Busca tradicional origem/destino/data como fluxo principal, reserva e pagamento, contas de usuário, buscas salvas, alertas de preço, itinerários multi-trecho, integração com fonte real de dados de voo.

## 6. Resultado esperado

Um usuário consegue, sem sair da tela inicial, dizer quanto quer gastar e receber destinos plausíveis dentro do orçamento — mesmo que os dados ainda sejam de exemplo.

## 7. Status

**Concluído** (tag `v0.1.0`). Os itens 4.1–4.4 foram implementados com dados mock (frontend e backend). Detalhe em [ACCEPTANCE.md](ACCEPTANCE.md) e [../AUDIT_V0.1.md](../AUDIT_V0.1.md).
