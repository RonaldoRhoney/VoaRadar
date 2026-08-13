# Voa Radar v0.3 — Critérios de Aceite

## Banco

- [x] Supabase/PostgreSQL configurado.
- [x] Migration funcionando (`alembic upgrade head` aplicado no projeto real).
- [x] Rollback testado (`alembic downgrade -1` limpa tudo, `upgrade head` reaplica sem erro).
- [ ] Dados persistidos (schema criado; nenhum dado gravado ainda — entra na FASE 3/4).

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
- [ ] Sem afirmações enganosas.

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

- [ ] Unitários.
- [ ] Integração.
- [ ] API.
- [ ] E2E.

## Regressão

- [ ] v0.2 continua funcionando.

## Segurança

- [ ] Secrets fora do Git.
- [ ] `.env.example` atualizado.
- [ ] Credenciais não expostas.

## Documentação

- [ ] README.
- [ ] Context.
- [ ] Roadmap.
- [ ] Decisions.

## Release

- [ ] Commit.
- [ ] Tag `v0.3.0`.
- [ ] Push.
