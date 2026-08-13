# Voa Radar v0.3 — Critérios de Aceite

## Banco

- [x] Supabase/PostgreSQL configurado.
- [x] Migration funcionando (`alembic upgrade head` aplicado no projeto real).
- [x] Rollback testado (`alembic downgrade -1` limpa tudo, `upgrade head` reaplica sem erro).
- [x] Dados persistidos (checkbox estava desatualizado — confirmado agora: 5 airports, 3 airlines, 4 routes, 9 flight_observations, 18 price_snapshots no Supabase real).

## Histórico

- [x] Observações armazenadas (`scripts/seed_history.py` gravou 9 no Supabase real).
- [x] Histórico não sobrescrito (rodar o coletor 2x: 9 `flight_observations` continuam 9, `price_snapshots` dobra pra 18 — cada rodada soma um preço novo, não substitui).
- [x] Timestamp armazenado (`observed_at` em cada `price_snapshot`).
- [x] Provider identificado (`provider="mock"` em cada `flight_observation`).

## Analytics

- [x] Mínimo.
- [x] Máximo.
- [x] Média.
- [x] Mediana (testado que não é puxada por outlier como a média é).
- [x] Variação (`percentage_vs_mean`, `percentage_vs_min`).
- [x] Score (posição relativa mín–máx, 0–100).
- [x] Confiança (LOW/MEDIUM/HIGH por tamanho de amostra).

## Inteligência

- [x] Score determinístico (mesmo input → mesmo output, testado).
- [x] Dados insuficientes tratados (0 observações → `has_sufficient_data=False`; poucas observações → stats calculadas normalmente, mas `confidence=LOW`).
- [x] Sem previsão de futuro.
- [x] Sem afirmações enganosas (verificado: grep por "compre agora"/"vai subir"/"menor preço do mercado" — zero ocorrências; texto sempre inclui "Análise baseada no histórico disponível pelo Voa Radar").

## API

- [x] Endpoint funcionando (`GET /flights/price-intelligence/{offer_id}?price=X`, validado ao vivo contra o Supabase real).
- [x] Schema validado (`price` obrigatório e `> 0`, 422 caso contrário).
- [x] Erros tratados (oferta sem histórico → 404 com mensagem amigável, nunca 500 cru).
- [x] Dados normalizados (resposta é o schema `PriceIntelligence`, nunca expõe modelo interno do banco).

## Frontend

- [x] Preço atual.
- [x] Média.
- [x] Mínimo.
- [x] Máximo.
- [x] Score.
- [x] Confiança.
- [x] Gráfico (SVG próprio, sem biblioteca — só aparece com 2+ pontos de histórico).
- [x] Explicação ("O preço atual está X% em relação à média observada").

## UX

- [x] Mobile (390px, validado).
- [x] Desktop (1280px, validado).
- [x] Loading (skeleton).
- [x] Empty (oferta sem histórico → "ainda não temos dados suficientes", distinto de erro).
- [x] Error (mensagem amigável, testado).
- [x] Dados insuficientes (`confidence=LOW` → aviso "ainda estamos aprendendo esta rota", número não escondido).

## Testes

- [x] Unitários (analytics engine, 14 testes puros).
- [x] Integração (repository + collector contra SQLite, 10 testes).
- [x] API (endpoint de price-intelligence, 6 testes incluindo validação de `inf`/`nan`).
- [x] E2E (checkbox estava desatualizado — só existia validação manual avulsa; teste comitado agora em `tests/e2e/explore-search.spec.ts`, 3/3 passando).

## Regressão

- [x] v0.2 continua funcionando (2/2 E2E, fluxo completo Home → resultados → detalhe, sem erro de console).

## Segurança

- [x] Secrets fora do Git (verificado no diff de cada commit da v0.3, incluindo o `DATABASE_URL` com senha).
- [x] `.env.example` atualizado (`DATABASE_URL` com placeholder).
- [x] Credenciais não expostas.
- [x] Entrada validada contra XSS (`offer_id` com `<script>`), valores não-finitos (`inf`/`nan` — achado e corrigido nesta auditoria), preço fora de faixa realista, e tipo errado — tudo 404/422 estruturado, nunca 500 cru.
- [x] RLS habilitado nas 5 tabelas + grants de `anon`/`authenticated` revogados (achado crítico: acesso público de leitura/escrita/exclusão direto pelo Supabase, sem passar pelo backend — ver [AUDIT_SECURITY.md](AUDIT_SECURITY.md)).
- [x] Regras de negócio confirmadas centralizadas no backend — nenhum cálculo de score/classificação/orçamento no frontend.

## Documentação

- [x] README.
- [x] Context.
- [x] Roadmap.
- [x] Decisions.

## Release

- [x] Commit.
- [x] Tag `v0.3.0`.
- [x] Push.

> Nota: 2 commits de segurança (`b36e624`, `a7c698b`) entraram **depois** da tag `v0.3.0` — o código em `main` está mais seguro do que o commit que a tag aponta. Ver pergunta ao usuário sobre cortar `v0.3.1`.
