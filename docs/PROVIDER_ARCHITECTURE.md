# PROVIDER_ARCHITECTURE.md — Voa Radar

> Discovery/projeto de arquitetura, 2026-08-16 — a partir da proposta do Ronaldo de formalizar "RhoneyInc Zero-Cost API First" como decisão arquitetural, depois de `DATA_SOURCES.md`/`API_LIMITS.md`/`LICENSES.md` corrigirem 2 premissas erradas da proposta original (Amadeus Self-Service descontinuado, OpenSky/Aviationstack sem dado de preço). **Documento de planejamento — nenhuma linha de código foi alterada.** Aguardando aprovação antes de qualquer implementação, conforme pedido explícito.

## 1. Estado atual (verificado no código, não suposto)

`FlightProvider` já é uma interface abstrata desde a v0.1 (`backend/app/providers/base.py`) — `get_destinations(origin_city, month) -> list[RawDestination]`. Único provider real hoje: `MockFlightProvider`. A abstração multi-provider **já existe**, não precisa ser criada do zero — o que falta é (a) um segundo provider de verdade implementando essa interface, e (b) um mecanismo separado pra dado de **referência** (ANAC), que não é a mesma coisa que um `FlightProvider` de oferta.

## 2. Distinção importante: provider de oferta vs. fonte de referência

`FlightProvider` devolve **ofertas específicas e compráveis** (preço, data, escalas, companhia) — é isso que `MockFlightProvider` simula e é isso que alimenta a busca por orçamento. A ANAC **não** devolve isso — devolve tarifa **média mensal por rota**, histórica. Tentar encaixar a ANAC na interface `FlightProvider` seria enganoso (implicaria "esta é uma oferta", quando é uma média estatística). Por isso, a arquitetura proposta trata a ANAC como um componente **diferente**:

```text
                    Voa Radar
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    FlightProvider              FareReferenceProvider
   (oferta comprável)          (referência histórica)
          │                           │
   MockFlightProvider              ANAC
   (único hoje, real)          (mensal, CSV)
          │                           │
          ▼                           ▼
    Price Intelligence  ←──── enriquece a análise
   (Analytics Engine, já existe)
          │
          ▼
       Supabase
          │
          ▼
     Radar Engine
```

`FareReferenceProvider` é uma interface nova, pequena — um método (`get_average_fare(origin, destination, month) -> float | None`), implementada por `AnacFareProvider`. Nunca gera oferta, nunca aparece como "disponível pra compra" — só alimenta o Analytics Engine como mais um sinal (ex: "preço atual R$ 429, média histórica ANAC pra essa rota R$ 480 → abaixo da média").

## 3. O que muda de verdade nesta etapa

- **`MockFlightProvider` continua sendo o único `FlightProvider`** — nenhum provider real de oferta é implementado agora (Amadeus está morto, nenhum outro foi aprovado).
- **ANAC entra como `FareReferenceProvider`**, `cost_status = ZERO_COST` — único componente novo com dado externo real nesta etapa.
- **Duffel/Amadeus Enterprise/outro provider de oferta real**: interface `FlightProvider` já suporta, mas nenhuma implementação nova é feita — ficam `BLOCKED`, mesmo padrão da skill `zero-cost-api`.

## 4. Database impact

Tabela nova, aditiva, sem alterar `Airport`/`Airline`/`Route`/`FlightObservation`/`PriceSnapshot` existentes:

```text
anac_fare_reference (novo)
  id, route_id (fk routes), reference_month (ex: "2026-06"),
  average_fare numeric, sample_size int (se disponível no CSV),
  source_url text, imported_at timestamptz, created_at timestamptz
```

Sem migração de dado existente — tabela nova, populada por um script offline (mesmo padrão de `scripts/seed_history.py`), não em runtime.

## 5. Impacto na v0.4

Nenhum. Radar Engine, notificações, auth/admin (`FASE A` em andamento) não mudam de comportamento — a ANAC só adiciona um sinal a mais no Price Intelligence (`app/analytics/`), que já é consumido pelo Radar Engine indiretamente via `PriceIntelligenceService`. Nenhuma tabela/rota/regra de negócio existente é alterada.

## 6. Quais APIs serão realmente implementadas

Só uma: **ANAC**, como `FareReferenceProvider`, `ZERO_COST`. Nenhuma outra fonte externa entra nesta etapa — nem Amadeus (não existe mais), nem OpenSky/Aviationstack (não servem), nem nenhum provider comercial (sem aprovação).

## 7. Decisão arquitetural a registrar

**"RhoneyInc Zero-Cost API First"** — todo produto RhoneyInc segue a skill `zero-cost-api` (`MyApps/.claude/skills/zero-cost-api/SKILL.md`) antes de integrar qualquer fonte externa nova. Voa Radar é o primeiro produto a formalizar isso, motivado por uma verificação real que corrigiu a premissa da proposta original (Amadeus morto, OpenSky/Aviationstack sem o dado certo).

## 8. Comunicação ao usuário — correção de promessa

Não prometer "o Voa Radar consulta Azul/GOL/LATAM diretamente" — nenhuma integração com companhia aérea existe ou está planejada nesta etapa. A comunicação correta, já sugerida na proposta original: **"O Voa Radar combina fontes públicas e provedores de dados de aviação para encontrar e analisar oportunidades de viagem."** Quando os dados forem exibidos, indicar a fonte (ex: "Fonte: ANAC — atualização mensal" vs. dado do provider de oferta em uso).

## 9. Testes propostos (a implementar quando aprovado, não implementados ainda)

Provider selection/fallback, quota exhaustion → `DISABLED`, timeout, API failure, invalid response, normalização, dedup de oferta, `cost_status`, provider desabilitado, fallback pro Mock. Cenários específicos: ANAC indisponível → Price Intelligence continua funcionando só com o histórico próprio (nunca quebra); provider pago tentado sem aprovação → bloqueado por configuração, não por exceção em runtime.

## 10. Roadmap proposto

| Etapa | O que é | Depende de decisão nova? |
|---|---|---|
| PA.1 | `FareReferenceProvider` (interface) + `AnacFareProvider` (implementação) | Não |
| PA.2 | Tabela `anac_fare_reference` + script de importação offline (CSV → Supabase) | Não |
| PA.3 | `PriceIntelligenceService` passa a considerar a referência ANAC quando disponível pra rota | Não |
| PA.4 | Frontend: indicação de fonte visível ("Fonte: ANAC, atualização mensal" vs. "Mock/dado de demonstração") | Não |
| PA.5 (futuro) | Provider de oferta real (Amadeus Enterprise, Duffel, outro) | Sim — decisão de orçamento explícita, fora do escopo desta etapa |

## 11. Status

Documento de projeto. Nenhuma implementação autorizada — aguardando aprovação, conforme pedido explícito.
