# LICENSES.md — Voa Radar

> Discovery, 2026-08-16. Licença de cada fonte de dado externo em uso ou avaliada — ver `DATA_SOURCES.md` pro contexto completo de cada uma.

## ANAC — Dados Abertos (Tarifas Aéreas)

- **Licença explícita**: não identificada uma licença nomeada (tipo CC0/CC-BY/ODbL) no conteúdo verificado da página oficial — só a categorização "dado aberto" dentro da Lei de Acesso à Informação (LAI) e da política brasileira de dados abertos governamentais.
- **Uso comercial**: dado público governamental, sem restrição explícita de uso comercial encontrada — mas, na ausência de licença nomeada, a prática recomendada é **atribuição visível da fonte** sempre que o dado aparecer na interface do produto, mesmo sem exigência formal confirmada.
- **Ação recomendada**: exibir "Fonte: ANAC — Tarifas Aéreas Domésticas, atualização mensal" em qualquer tela que use esse dado (mesma prática já sugerida na seção de credibilidade do produto). Nunca apresentar como "preço disponível pra compra agora".

## `MockFlightProvider`

- Dado sintético, gerado internamente — sem questão de licença (não é dado de terceiro).

## Fontes descartadas — licença registrada, sem uso

| Fonte | Licença | Observação |
|---|---|---|
| OpenSky Network | Gratuita **só para uso não-comercial/pesquisa** — uso comercial exigiria licença separada, não avaliada aqui porque a fonte já foi descartada por não ter o dado necessário. | Registrado como impeditivo adicional, não só "dado errado". |
| Aviationstack | Termos de uso do free tier não avaliados em detalhe (fonte descartada antes por não ter o dado). | — |
| Amadeus Self-Service | Portal (e portanto seus termos de uso self-service) não existe mais desde 17/jul/2026. | — |

## Regra geral aplicada (skill `zero-cost-api`)

Nenhuma fonte entra em produção sem licença conferida contra o uso pretendido — "está disponível publicamente" nunca é, por si só, sinônimo de "podemos usar do jeito que queremos". Quando a licença não é clara (caso da ANAC), a prática mais segura é atribuição visível + nunca apresentar o dado de um jeito que sugira mais autoridade/atualidade do que ele realmente tem.
