# API_LIMITS.md — Voa Radar

> Discovery, 2026-08-16. Limites reais das fontes viáveis (ver `DATA_SOURCES.md` — as demais candidatas foram descartadas antes de chegar a este nível de detalhe, por não servirem ao propósito ou não existirem mais).

## ANAC — Dados Abertos (Tarifas Aéreas)

- **Método de acesso**: download direto de arquivo CSV via `gov.br/anac` (área "Voos e operações aéreas" → "Tarifas Aéreas Domésticas"/"Internacionais"). Sem autenticação, sem token, sem chave de API.
- **Limite de requisição**: nenhum limite de quota conhecido — é download de arquivo estático, não uma API de consulta em tempo real por chamada.
- **Frequência de atualização real**: mensal (o painel/CSV é republicado periodicamente, dado retroativo a 2002 pra série doméstica).
- **Formato**: CSV, com filtros pra extração no próprio portal.
- **Risco de cobrança**: nenhum — arquivo público, sem chave, sem quota paga.
- **`cost_status`**: `ZERO_COST`.

## `MockFlightProvider` (já existe)

- Sem limite — dado sintético, gerado localmente.
- **`cost_status`**: `ZERO_COST`.

## Fontes descartadas (registradas aqui só pra não precisar reavaliar do zero no futuro)

| Fonte | Limite real (quando existia/existe) | Motivo do descarte |
|---|---|---|
| Amadeus Self-Service Test | Tinha quota mensal gratuita real, mas o portal foi descontinuado em 17/jul/2026 | Provedor não existe mais |
| OpenSky Network | Gratuita, uso não-comercial | Não fornece preço, é rastreamento de posição |
| Aviationstack | 100 requisições/mês no free tier | Não fornece preço em nenhum plano |
| `dados.gov.br` API (CKAN) | Requer token pessoal — `401 Bearer` confirmado em toda chamada, mesmo leitura simples | Desnecessário — ANAC direto não precisa dessa fricção |

## Revisão futura

Se/quando um provider comercial de oferta real for aprovado (Amadeus Enterprise, Duffel, outro), este documento precisa de uma entrada nova com quota/pricing real confirmado na fonte primária antes de qualquer integração — nunca reaproveitar número de memória ou resumo de terceiro sem checar de novo (mesma lição que motivou a skill `zero-cost-api`).
