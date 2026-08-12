# Auditoria — Voa Radar v0.1

Data: 2026-08-12. Escopo: todos os arquivos do projeto (`frontend/`, `backend/`, docs, protótipo), antes de congelar a v0.1.

## O que foi testado

- Suíte de testes do backend (`pytest`, dentro de `backend/.venv`).
- Suíte de testes unitários do frontend (`npm run test`, Vitest).
- Teste E2E ponta a ponta (`npx playwright test`), com backend e frontend reais rodando juntos.
- `npm run build` (type-check + build de produção do frontend).
- Fluxo completo no navegador, capturado em screenshots reais (não mockup): Home (desktop e mobile), resultados carregando, resultados com sucesso, detalhe da oportunidade, resultados vazio, resultados com erro (backend derrubado de propósito).
- Varredura de arquivos do repositório inteiro: imports mortos, referências quebradas, segredos no código, consistência entre `.env.example` e `core/config.py`.

## O que passou

- Backend: 5/5 testes `pytest` (health check, busca dentro do orçamento, lista vazia quando nada cabe, validação de orçamento inválido, service delegando pro provider injetado).
- Frontend: 3/3 testes Vitest (`formatCurrencyBRL`, `useBudgetSearch` em sucesso e erro).
- E2E: 1/1 (Home → resultados → detalhe da oportunidade, com o backend real respondendo).
- `npm run build` sem erros de tipo.
- Nenhum secret, API key ou senha encontrado no código.
- `.env.example` (frontend e backend) consistentes com as variáveis realmente lidas em `core/config.py`.
- `PRD.md` conferido contra o que foi implementado — segue consistente, sem necessidade de ajuste.

## Problemas encontrados e corrigidos nesta sessão

| Problema | Causa | Correção |
|---|---|---|
| E2E falhava com "strict mode violation" | `getByText("Voa Radar")` batia em 4 elementos (header, h1, footer, copyright) | Trocado para `getByRole("heading", { name: "Voa Radar" })` |
| Vitest tentava rodar o spec do Playwright | Sem `include` explícito no config do Vitest, ele varria `tests/e2e/*.spec.ts` também | `vite.config.ts` → `test.include: ['src/**/*.test.ts', 'src/**/*.test.tsx']` |
| `<html lang="en">` e `<title>frontend</title>` | Nunca customizados desde o scaffold do Vite | `lang="pt-BR"`, `<title>Voa Radar</title>` |
| Favicon genérico do template Vite | Nunca substituído pela identidade do produto | Novo `favicon.svg` (radar + rota de voo, cores do próprio app) |
| Código morto: `public/icons.svg`, `src/assets/vite.svg` | Resíduo do scaffold, sem nenhuma referência no código | Removidos |
| Sem rota "não encontrada" | `App.tsx` só tinha `/` e `/resultados` — URL errada caía em tela branca | Adicionada `NotFound.tsx` + rota catch-all (`*`) |
| `BudgetSearchRequest.budget` sem validação mínima | Dava pra mandar `budget: 0` ou negativo direto pela API (UI limitava via slider, API não) | `Field(gt=0)` no schema + teste cobrindo o caso |

## Pendências (não resolvidas, registradas conscientemente)

- **Banco de dados**: ainda não conectado — decisão de escopo em aberto com o usuário (mover só os destinos mock pro Postgres/Supabase vs. guardar histórico de busca vs. outra coisa). Ver [docs/DECISIONS.md](DECISIONS.md).
- **Botão "Como Usar"**: pedido pelo usuário, ainda não implementado — falta definir o que "ajustado de acordo com o progresso do App" significa na prática antes de construir.
- **Componentes React sem teste unitário próprio** (`BudgetSearchForm`, `Results`) — cobertos indiretamente pelo E2E, não por Testing Library isolado. Registrado como decisão aceita em sessão anterior (ver [DECISIONS.md](DECISIONS.md)), não um problema novo.
- **`GitHub` não refletia o código mais recente** até esta sessão — corrigido: tudo commitado e enviado (`33514cc`, `HEAD` no momento desta auditoria).

## Riscos conhecidos

- `MockFlightProvider` ignora `origin_city`/`month` no filtro — o mesmo conjunto de 4 destinos aparece pra qualquer origem/mês, documentado no docstring do provider. Não é bug, é limitação conhecida do estágio mock.
- Nenhum rate limit ou proteção contra abuso no endpoint `/flights/budget-search` — aceitável para v0.1 local/não pública, vira risco real assim que houver deploy.
- Deploy, Supabase e banco de dados: nada provisionado. v0.1 roda só local.

## Conclusão da auditoria

**v0.1 está estável e consistente**: frontend, backend, testes (unitários + E2E) e documentação alinhados entre si e com o código real, sem código morto relevante restante e sem segredo exposto. Os 7 problemas encontrados foram corrigidos e verificados na mesma sessão. As pendências que restam são decisões de escopo em aberto (banco de dados, botão "Como Usar"), não bugs.

**Recomendação**: congelar e marcar `v0.1.0` como o primeiro ponto de fundação funcional do Voa Radar.
