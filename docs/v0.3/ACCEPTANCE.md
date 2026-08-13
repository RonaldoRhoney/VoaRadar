# Voa Radar v0.3 — Critérios de Aceite

## Banco

- [x] Supabase/PostgreSQL configurado.
- [x] Migration funcionando (`alembic upgrade head` aplicado no projeto real).
- [x] Rollback testado (`alembic downgrade -1` limpa tudo, `upgrade head` reaplica sem erro).
- [ ] Dados persistidos (schema criado; nenhum dado gravado ainda — entra na FASE 3/4).

## Histórico

- [ ] Observações armazenadas.
- [ ] Histórico não sobrescrito.
- [ ] Timestamp armazenado.
- [ ] Provider identificado.

## Analytics

- [ ] Mínimo.
- [ ] Máximo.
- [ ] Média.
- [ ] Mediana.
- [ ] Variação.
- [ ] Score.
- [ ] Confiança.

## Inteligência

- [ ] Score determinístico.
- [ ] Dados insuficientes tratados.
- [ ] Sem previsão de futuro.
- [ ] Sem afirmações enganosas.

## API

- [ ] Endpoint funcionando.
- [ ] Schema validado.
- [ ] Erros tratados.
- [ ] Dados normalizados.

## Frontend

- [ ] Preço atual.
- [ ] Média.
- [ ] Mínimo.
- [ ] Máximo.
- [ ] Score.
- [ ] Confiança.
- [ ] Gráfico.
- [ ] Explicação.

## UX

- [ ] Mobile.
- [ ] Desktop.
- [ ] Loading.
- [ ] Empty.
- [ ] Error.
- [ ] Dados insuficientes.

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
