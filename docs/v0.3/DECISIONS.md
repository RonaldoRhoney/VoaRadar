# Voa Radar v0.3 — Decisões

## DEC-001 — Não reconstruir a v0.2

A v0.3 evolui a fundação existente.

## DEC-002 — PostgreSQL passa a fazer parte da aplicação

**Motivo**: a v0.3 necessita de persistência histórica.

## DEC-003 — Histórico não será sobrescrito

Cada observação é preservada.

## DEC-004 — Destination, Offer e PriceObservation são conceitos diferentes

Continuidade da separação já estabelecida na v0.2 (DEC-009 de `docs/v0.2/DECISIONS.md`).

## DEC-005 — Analytics engine separado da API

## DEC-006 — O frontend não calcula o score

O backend é responsável pela inteligência; o frontend só apresenta.

## DEC-007 — O score não representa previsão

## DEC-008 — Dados insuficientes reduzem a confiança

## DEC-009 — A v0.3 não depende de um provider real específico

**Motivo**: instabilidade recente sinalizada no acesso self-service do Amadeus, e a API de "Cheapest Date Search" deles é baseada em cache pré-computado — dinâmica diferente da busca ao vivo. O motor de inteligência não deve depender de qual fornecedor será usado no futuro.

## DEC-010 — Nenhuma integração de scraping

## DEC-011 — Nenhuma funcionalidade de booking

## DEC-012 — Moeda explícita, nunca assumir BRL permanentemente

## DEC-013 — Banco de dados via Supabase (não Postgres genérico/Docker local)

**Motivo**: decisão do usuário — consistente com o padrão já usado por todo o resto do ecossistema RhoneyInc (MeuPet, MenuFlex, AmaVida...). Resolve a pendência em aberto desde a auditoria da v0.1 (`docs/AUDIT_V0.1.md`, seção "Pendências") sobre onde/como conectar banco de dados.

## Problema encontrado e corrigido — FASE 2 (conexão real)

`alembic upgrade head` falhava com `ValueError: invalid interpolation syntax` ao processar a `DATABASE_URL`. Causa: a senha do banco tem caracteres especiais (`@`) percent-encoded como `%40`, e `Config.set_main_option()` do Alembic passa o valor pelo `configparser`, que interpreta `%` como início de sintaxe de interpolação (`%(nome)s`).

**Solução**: `alembic/env.py` deixou de usar `config.set_main_option("sqlalchemy.url", ...)` + `engine_from_config` (que dependem do `configparser`) e passou a criar a engine diretamente com `sqlalchemy.create_engine(DATABASE_URL, ...)`, lendo a URL direto de `app.core.config` — nunca mais passa pelo parser de `.ini`. Testado de ponta a ponta: `upgrade head` → 5 tabelas criadas no Supabase real → `downgrade -1` limpa tudo → `upgrade head` reaplica sem erro.

## DEC-014 — Uuid portável e defaults em Python, não específicos do Postgres

Os models usam `sqlalchemy.Uuid(as_uuid=True)` (genérico) em vez de `sqlalchemy.dialects.postgresql.UUID`, e `default=uuid.uuid4`/`default=utcnow` (Python) em vez de `server_default=text("gen_random_uuid()")`/`text("now()")` (específicos do Postgres).

**Motivo**: permite rodar os testes de repository contra SQLite em memória — rápido, sem tocar no Supabase real a cada `pytest`, mesma filosofia de teste que o resto do projeto já usa (providers fake, sem rede). No Postgres em produção o comportamento é idêntico. A migration (`0001_price_intelligence_schema.py`) continua com `postgresql.UUID`/`gen_random_uuid()` nativos no DDL — isso é intencional, o DDL alvo é sempre Postgres; só o lado ORM/Python precisava ser portável.

## DEC-015 — Diretório de aeroportos/companhias mock vive no Collector, não no Provider

`app/collectors/airport_directory.py` resolve nome de cidade → código de aeroporto e nome de companhia → código, só pra alimentar o banco a partir dos dados fictícios do `MockFlightProvider`.

**Motivo**: manter o contrato de `FlightProvider` limpo — um provider real (Amadeus, Duffel) já devolveria código IATA e código de companhia prontos, não precisaria dessa ponte. Isolar essa resolução no Collector evita vazar uma preocupação exclusiva do estágio mock para a interface que providers reais vão implementar depois.

## DEC-016 — Fórmula do score: posição relativa dentro do intervalo mín–máx

```python
if maximum == minimum:
    score = 50  # sem variação histórica, neutro
else:
    position = (current_price - minimum) / (maximum - minimum)
    score = round((1 - position) * 100)  # 0=mais caro já visto, 100=mais barato já visto
```

Confirmada na análise A–K da FASE 2 (proposta na seção F), implementada e testada em `app/analytics/engine.py` — inclusive os casos de fronteira (preço no mínimo → 100, no máximo → 0, ponto médio → 50, sem variação → 50, preço atual fora da faixa histórica → limitado a 0–100).

## DEC-017 — Poucos dados não é "sem dados"

`sample_size == 0` é o único caso que zera as estatísticas (`has_sufficient_data=False`). Com 1+ observações, o motor calcula normalmente (mínimo/máximo/média/score), só marca `confidence=LOW` quando `sample_size < 10`.

**Motivo**: `UX.md` §3 mostra o exemplo "Ainda estamos aprendendo esta rota — 8 observações", ou seja, ainda mostra os dados junto do aviso de confiança baixa — não esconde o número, hedgeia a linguagem. Essa interpretação foi registrada aqui porque o `PRICE_INTELLIGENCE.md` §11 poderia ser lido como "não calcular nada com poucos dados"; optei pela leitura mais fiel ao UX.md.

## Problema encontrado e corrigido — FASE 7 (testes de API)

Os testes de `GET /flights/price-intelligence/{offer_id}` falhavam com `no such table: flight_observations`, mesmo com os dados semeados no mesmo `db_session` do teste. Causa: o `TestClient` do FastAPI roda rotas síncronas numa thread de worker (via threadpool do Starlette), e `sqlite:///:memory:` isola o banco por conexão — cada conexão nova (inclusive de outra thread) enxerga um banco vazio, mesmo dentro do "mesmo" `:memory:`.

**Solução**: engine de teste passou a usar `poolclass=StaticPool` + `connect_args={"check_same_thread": False}`, forçando todas as conexões (não importa a thread) a compartilhar a mesma conexão/banco em memória. Fixture `client` em `conftest.py` sobrescreve `get_db` pra usar esse mesmo `db_session` via `app.dependency_overrides`.

## Endpoint

`GET /flights/price-intelligence/{offer_id}?price=X` — sem prefixo `/api/v1/` (DEC confirmada na FASE 2), `price` obrigatório e validado (`gt=0`), 404 amigável quando a oferta não tem histórico coletado. Validado ao vivo contra o Supabase real (`offer-rec-001` → score 100/EXCELLENT).

## DEC-018 — `history` (série bruta) entra no schema `PriceIntelligence`

O `PRICE_INTELLIGENCE.md` original só especificava estatísticas agregadas (mínimo/máximo/média/mediana/score/confiança) como saída do motor — nada de série temporal. Mas o `UX.md` §5 e o `IMPLEMENTATION.md` FASE 8 pedem um gráfico de histórico, que precisa de pontos (preço + data), não só agregados.

**Decisão**: `PriceIntelligenceService` busca a série bruta via `repository.get_price_history_points()` (novo método) e anexa em `PriceIntelligence.history`, separado das estatísticas — o `analytics.engine` continua recebendo só a lista de preços, sem saber de datas, mantendo-se puro. `history` só serve pro gráfico; a análise em si nunca depende dele.

## DEC-019 — Gráfico em SVG próprio, sem biblioteca de charts

`PriceHistoryChart.tsx` desenha um polyline + pontos à mão (viewBox fixo, sem eixo de escala além de min/máx do próprio histórico), com tooltip nativo via `<title>` do SVG — sem `recharts`/`chart.js`/etc.

**Motivo**: consistente com o resto do frontend (sem dependências além do estritamente necessário — `exploreFilters.ts` também é lógica pura sem lib). Só aparece com 2+ pontos de histórico (com 1 ponto não há linha pra desenhar).

## DEC-020 — Rótulos de classificação/confiança (não especificados literalmente no PRD)

O PRD dava só o exemplo "🟢 Boa oportunidade" pra `GOOD`. Defini os demais: `EXCELLENT`="🟢 Excelente oportunidade", `NORMAL`="🟡 Preço normal", `EXPENSIVE`="🟠 Acima da média", `VERY_EXPENSIVE`="🔴 Preço alto". Confiança seguiu literal o `UX.md` §7 (🟢/🟡/⚪).

## Problema encontrado e corrigido — FASE 10 (auditoria)

`GET /flights/price-intelligence/{offer_id}?price=inf` (ou `nan`) derrubava a API com `500 Internal Server Error` cru — violação direta da seção 15 do `CLAUDE.md` (nunca expor erro técnico). Causa: `Query(..., gt=0)` aceita `inf` (matematicamente `inf > 0` é verdadeiro) e `nan` só é barrado por acidente em alguns casos; o valor seguia até `_score_from_position()`, onde `round((1 - inf) * 100)` lança `OverflowError` (Python não converte infinito pra `int`).

**Solução**: `Query(..., gt=0, lt=1_000_000, allow_inf_nan=False, ...)` — rejeita `inf`/`nan`/`-inf` na validação (422, mensagem estruturada do Pydantic) e limita a um teto realista de preço. 2 testes novos cobrindo `inf`/`-inf`/`nan` e valor acima do limite. Achado testando deliberadamente valores extremos na auditoria, não apareceu em nenhum teste "feliz" anterior.
