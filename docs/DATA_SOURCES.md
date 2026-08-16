# DATA_SOURCES.md — Voa Radar

> Discovery, 2026-08-16 — avaliação de fontes de dado externo candidatas, seguindo a skill RhoneyInc `zero-cost-api` (`MyApps/.claude/skills/zero-cost-api/SKILL.md`). **Nenhuma linha de código foi alterada.** Toda fonte abaixo foi verificada de verdade (`curl`/busca na fonte primária), não assumida a partir de resumo de terceiro — corrigiu 2 premissas erradas da proposta original antes de qualquer arquitetura ser desenhada.

## Resumo executivo

Das 4 fontes avaliadas como candidatas a **provider de preço de passagem**, só 1 é viável — e mesmo essa não fornece preço em tempo real, só referência histórica. **Não existe hoje nenhuma API gratuita/baixo-custo que entregue tarifa comercializável em tempo real pro Brasil.** Isso não muda o objetivo do Voa Radar, muda o que dá pra implementar nesta etapa: `MockFlightProvider` continua como único provider de oferta; ANAC entra como enriquecimento real do Price Intelligence.

## Fontes avaliadas

| Fonte | Papel pretendido | Verificação real | `cost_status` |
|---|---|---|---|
| **ANAC — Dados Abertos (Tarifas Aéreas Domésticas/Internacionais)** | Referência histórica/enriquecimento | Confirmado: download CSV direto no site oficial da ANAC (`gov.br/anac`), sem autenticação, sem token — mais simples que passar pelo `dados.gov.br` (ver nota abaixo). Dado retroativo a 2002, atualização mensal. | `ZERO_COST` |
| **Amadeus for Developers — Self-Service (Test)** | Provider de oferta (teste) | **Descontinuado de vez em 17/jul/2026** — confirmado por múltiplas fontes independentes (PhocusWire, LinkedIn, TravelTrade News). Registro de novos usuários pausado desde fevereiro/2026, chaves existentes desativadas na data do desligamento. Não é "ambiente de teste ainda disponível" — o portal self-service inteiro não existe mais. | `BLOCKED` (provedor não existe mais, não é uma questão de aprovação) |
| **OpenSky Network** | Provider de oferta/enriquecimento | API real, gratuita, mas **nunca forneceu preço de passagem** — só posição/altitude/velocidade via ADS-B (rastreamento de aeronave). Licença também restringe a uso não-comercial/pesquisa. | `BLOCKED` (dado errado pro propósito, e licença não cobre uso comercial) |
| **Aviationstack** | Provider de oferta/enriquecimento | Free tier real (100 req/mês), mas **não inclui preço/tarifa em nenhum plano**, só status e horário de voo. | `BLOCKED` (dado errado pro propósito) |
| **`dados.gov.br` (API CKAN, caminho alternativo pra ANAC)** | Alternativa de acesso à ANAC | Testado de verdade (`curl`): `package_search`/`package_list` devolvem HTTP 401 com `www-authenticate: Bearer` — exige token pessoal em toda chamada. **Desnecessário** — ANAC direto (linha acima) já resolve sem essa fricção. | Não usado — ANAC direto é a via |
| **`MockFlightProvider`** (já existe) | Provider de oferta, fallback obrigatório | Já implementado desde v0.1, sem custo, sem dependência externa. | `ZERO_COST` |
| Amadeus Enterprise / Duffel / outro provider comercial | Provider de oferta real, futuro | Não avaliado em detalhe nesta rodada — sempre `PAID`/`BLOCKED` até aprovação explícita de orçamento, independente de quão "razoável" o preço pareça. | `BLOCKED` até decisão de negócio |

## Por que a arquitetura muda em relação à proposta original

A proposta original desenhava `FlightProvider` com ANAC + Amadeus Test + OpenSky como três fontes paralelas normalizadas. Com a verificação real: **Amadeus Test não existe mais**, e **OpenSky/Aviationstack nunca tiveram o dado necessário** (preço). Restam só duas fontes reais: `MockFlightProvider` (oferta, como já era) e ANAC (enriquecimento/referência histórica, papel que a própria proposta original já reservava corretamente pra ela — essa parte estava certa).

## Nota sobre licença da ANAC

A página oficial não expõe uma licença nomeada explicitamente (tipo CC0/CC-BY) no conteúdo verificado — só a categorização "dado aberto" dentro da política brasileira de dados abertos governamentais. Recomendação: **atribuir a fonte visivelmente** ("Fonte: ANAC — Tarifas Aéreas Domésticas") sempre que o dado for exibido, mesmo sem uma licença formal explícita — mesma disciplina já usada no KnowRa pra fonte governamental. Ver `LICENSES.md`.
