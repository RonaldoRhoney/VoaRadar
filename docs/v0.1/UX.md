# Voa Radar v0.1 — UX

> Documento retrospectivo — descreve a experiência como ela foi de fato construída na v0.1, no formato usado para planejar a v0.2.

## 1. Princípio

A interface deve responder rapidamente: "Para onde posso viajar com meu orçamento?"

## 2. Home

Hero: **✈️ Voa Radar** — "Diz pra gente quanto você quer gastar — a gente encontra pra onde dá pra ir."

## 3. Busca

Campos: quanto você quer gastar (slider R$ 200–5.000), de onde você quer sair (texto livre), quando você quer viajar (select de mês). Checkbox "Não sei para onde ir" (marcado por padrão). CTA: "Encontrar viagens".

## 4. Experiência de carregamento

Skeleton (3 blocos pulsantes) enquanto a busca está em andamento — nunca uma tela congelada.

## 5. Resultados

Cabeçalho: "🌎 Encontramos destinos que cabem no seu orçamento". Subtexto: "Saindo de Belém em Outubro · até R$ 800 · dados de exemplo (mock)".

## 6. Estado vazio

Nunca só "nenhum resultado" — mensagem própria ("Não encontramos destinos de exemplo dentro de R$ X. Tente aumentar o orçamento.").

## 7. Estado de erro

Mensagem amigável ("Não conseguimos encontrar destinos neste momento. Tente novamente em instantes." / "Não conseguimos falar com o servidor agora."), nunca um erro técnico cru — testado contra o backend real derrubado, não só lido no código.

## 8. Detalhe da oportunidade

Rota (origem → destino) e preço, com aviso "dados de exemplo (mock)".

## 9. Responsividade

Mobile-first, validado em 390px (mobile) e 1280px (desktop) com capturas reais do app.

## 10. Acessibilidade

Labels em todos os campos do formulário; `role="alert"`/`aria-live` nos estados de carregamento e erro.

## 11. Rodapé

Padrão RhoneyInc (skill `footer-padrao`): 4 colunas (Marca, Produto, RhoneyInc, Legal), mesma estrutura dos produtos-irmãos.
