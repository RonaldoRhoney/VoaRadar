# Voa Radar v0.2 — Decisões

## DEC-001 — Não reconstruir a v0.1

A v0.2 utilizará a fundação existente.

**Motivo**: a v0.1 foi auditada e aprovada (ver [../AUDIT_V0.1.md](../AUDIT_V0.1.md)).

## DEC-002 — Mock Provider continua

A v0.2 continuará utilizando `MockFlightProvider`.

**Motivo**: a UX precisa ser validada antes da integração com provedores reais.

## DEC-003 — Provider abstraction

A aplicação continuará utilizando `FlightProvider`.

**Motivo**: permitir múltiplos fornecedores futuramente sem acoplamento.

## DEC-004 — Sem PostgreSQL definitivo

A v0.2 não implementará persistência completa.

**Motivo**: histórico e usuários pertencem a versões futuras.

## DEC-005 — Orçamento como ponto central

A experiência Explore deve partir do orçamento.

**Motivo**: esse é o principal diferencial do Voa Radar.

## DEC-006 — Mobile-first

A experiência será desenvolvida priorizando dispositivos móveis.

**Motivo**: grande parte dos usuários utilizará smartphones.

## DEC-007 — Não implementar funcionalidades futuras

IA, alertas, autenticação e API real permanecem fora da v0.2.

**Motivo**: controle de escopo e qualidade.

## DEC-008 — Período simplificado nesta primeira implementação

Em vez de implementar "mês específico + intervalo + datas flexíveis" simultaneamente (como o PRD original de v0.2 sugere em 3.3), a primeira implementação prioriza **mês + flexibilidade básica**.

**Motivo**: validar primeiro o conceito central "orçamento → destinos" sem complicar a experiência de entrada. Análise de calendário completo (ex.: "qualquer dia entre 1 e 30 de outubro", o Voa Radar encontrando os melhores dias) fica para a v0.3, onde pode virar uma das experiências mais fortes do produto — não uma feature secundária espremida na v0.2.

## DEC-009 — Destino ≠ Oferta, com id próprio por oferta

`Destination` (id = código do aeroporto) e `Offer` (id próprio, ex.: `offer-rec-001`) são entidades separadas — um destino tem `bestOffer` + `offers[]`. O `FlightProvider` devolve destinos/ofertas crus (`RawDestination`), sem noção de orçamento; o `ExploreService` é quem classifica `budget_status` (`within_budget`/`near_budget`) e marca `highlight: "best_price"` só no destino mais barato retornado.

**Motivo**: decisão do usuário na revisão do contrato da FASE 2 — necessária para suportar múltiplas datas/preços por destino sem quebrar a modelagem depois.

## DEC-010 — Sem selo de "boa oportunidade" fabricado

Nenhum indicador de qualidade é calculado além de fatos verificáveis a partir da própria resposta: `budget_status` (dentro/perto do orçamento) e `highlight: "best_price"` (o mais barato *desta busca*). Nada de índice de oportunidade baseado em preço médio histórico, variação ou tendência.

**Motivo**: decisão explícita do usuário — "preço < orçamento" não significa boa oportunidade, e a v0.2 não tem histórico de preços pra calcular isso de verdade. `OpportunityScore` fica registrado como conceito para a v0.5 (ver `docs/v0.2/CONTEXT.md` §7), sem nenhum código dele agora.

## DEC-011 — Painel de filtros único (não sidebar desktop + bottom sheet mobile)

O UX.md §7 pedia sidebar/toolbar no desktop e bottom sheet no mobile. Implementei um único painel expansível (botão "Filtros" abre/fecha), igual nos dois breakpoints.

**Motivo**: evita depender de uma biblioteca de bottom sheet só para isso, mantendo a v0.2 pequena. Funciona nos dois tamanhos (validado em 390px/768px/1280px), mas é uma divergência consciente do desenho original, não uma omissão — fica registrado aqui para revisão futura caso o produto cresça a ponto de justificar o padrão completo.

## DEC-012 — Filtro de escalas simplificado a "somente voos diretos"

O PRD 3.8 previa filtros distintos para "sem escalas" e "uma escala". Implementei um único toggle "Somente voos diretos" (equivalente a "sem escalas"); não há filtro específico para "exatamente 1 escala".

**Motivo**: controle de escopo (regra 21 do `CLAUDE.md`) — o caso de uso mais comum ("eu não quero escala") está coberto; a distinção fina de quantidade de escalas pode entrar depois se um usuário real pedir.

## DEC-013 — Filtro de período não implementado na v0.2

O PRD 3.8 listava "período" como filtro dos resultados. Não implementei — o período já é definido na própria busca (mês), e filtrar de novo por período dentro dos resultados de um único mês não pareceu agregar nesta primeira fatia.

**Motivo**: a granularidade de período real (intervalo de dias) é o próprio escopo da v0.3 (DEC-008) — um filtro de período dentro da v0.2 seria redundante ou teria efeito quase nulo, dado que a busca já filtra por mês.

## DEC-014 — Margem de "próximo do orçamento"

`near_budget` inclui ofertas até R$ 100 acima do orçamento informado (`NEAR_BUDGET_MARGIN`, fixo no `ExploreService`).

**Motivo**: escolha pragmática para ter o comportamento do PRD 3.11/3.12 funcionando (nunca só "nenhum resultado"). Não validado com o usuário como valor definitivo — candidato a virar configurável ou a mudar de critério (ex.: "os 3 mais baratos acima do orçamento") se o valor fixo se mostrar errado na prática.
