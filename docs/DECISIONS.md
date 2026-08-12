# Diário de decisões — Voa Radar

Registro cronológico de arquitetura → decisões → código → problemas → soluções. Serve tanto de referência técnica quanto de material de portfólio (mostra o raciocínio, não só o resultado).

## 2026-08-12 — Bootstrap do projeto

**Decisão**: seguir o padrão RhoneyInc atual (não o mais antigo, tipo MeuPet): frontend React+TS+Vite+Tailwind, backend serverless/API própria, Supabase dedicado, deploy Vercel, repo GitHub próprio. Confirmado inspecionando os produtos-irmãos mais recentes (AmaVida, Fit-Now, MenuFlex) antes de propor.

**Decisão**: fonte de dados de voo será Amadeus for Developers (tier gratuito, self-service) — ainda não integrada, fica para uma fase seguinte.

**Problema identificado**: sessão não-interativa não tinha `gh` CLI nem token do GitHub disponível para criar o repositório remoto automaticamente.
**Solução**: usuário criou o repositório manualmente em github.com/new; Claude Code configurou o `origin` local (SSH) depois.

## 2026-08-12 — Tela prioritária: busca por orçamento

**Decisão do usuário**: a primeira experiência do produto não seria o formulário clássico (origem/destino/data), e sim um fluxo orçamento-primeiro: "quanto você quer gastar" → "de onde" → "quando" → destinos que cabem no valor. Isso substituiu o primeiro formulário construído (`SearchForm`/`InspireMe`, ainda no repo mas não usados na Home).

**Decisão**: dados mock explicitamente marcados no código (`MOCK DATA`, `budgetDestinationsMock`) tanto no frontend quanto no backend, para nunca serem confundidos com dado real mais adiante.

**Problema encontrado**: ao rodar o smoke test no navegador, a navegação (`<Link>`) quebrava com `Cannot destructure property 'basename' of ... null` — o `App` não estava envolto em `<BrowserRouter>` no `main.tsx`.
**Solução**: adicionado `BrowserRouter` em `main.tsx`. Fluxo completo (Home → resultados por orçamento → detalhe da oportunidade) validado via Playwright headless, sem erros de console — screenshots em `/tmp/voaradar-*.png` durante o desenvolvimento.

## Backend inicial

**Decisão do usuário**: backend em FastAPI (não Node/Vercel Functions como o padrão RhoneyInc mais recente usa) — estrutura modular (`app/config.py`, `app/models/`, `app/routers/`), health check, e um endpoint inicial (`POST /flights/budget-search`) já preparado com os mesmos modelos de dado do frontend, ainda usando mock.

**Sugestão futura**: decidir como esse FastAPI vai para produção (Vercel via runtime Python, ou outro host) — não decidido ainda, não implementado.
**Sugestão futura**: autenticação de usuário (contas, buscas salvas, alertas de preço) — fora do MVP, ver [PRD.md](../PRD.md).

## 2026-08-12 — Governança do projeto: CLAUDE.md formal + reestruturação para v0.1

**Decisão do usuário**: adoção de um `CLAUDE.md` detalhado (25 seções) formalizando regras já seguidas informalmente (não implementar ideia não pedida, não codificar sem plano, hierarquia de decisões, formato de comunicação Entendimento/Estado atual/Plano/Riscos) e definindo a arquitetura-alvo do projeto.

**Conflito identificado, não resolvido silenciosamente**: o documento fornecido pelo usuário usava "Roney Inc." em uma seção e "RhoneyInc." em outra — inconsistência interna. Sinalizado ao usuário, que confirmou **RhoneyInc** como o nome correto (consistente com o resto do ecossistema).

**Decisão**: reestruturação completa para bater com a arquitetura da seção 11 do `CLAUDE.md`:
- Backend: `app/api/` (rotas), `app/core/` (config), `app/schemas/` (Pydantic request/response), `app/services/` (regra de negócio, desacoplada do provider), `app/providers/` (`FlightProvider` abstrato + `MockFlightProvider` — preparando pra Amadeus/Duffel sem acoplar a nenhum ainda), `tests/`, `requirements/base.txt`+`requirements/dev.txt` (substituindo o `requirements.txt` único).
- Frontend: `features/budget-search/` (formulário + hook `useBudgetSearch`), `services/api.ts` (chamada real ao backend, com tratamento de erro), `utils/format.ts`, `tests/e2e/` (Playwright).
- **Ajuste informado, não silencioso**: não foi criada uma pasta `hooks/` vazia no frontend nem `app/models/` no backend — ainda não existe um hook genérico reaproveitável nem uma entidade de banco real, e a seção 12 do `CLAUDE.md` pede pra não criar estrutura antes de necessária.
- `SearchForm`/`InspireMe` (código morto desde a mudança pro fluxo de orçamento) removidos, por decisão do usuário.

**Problema encontrado ao rodar o E2E pela primeira vez**: `getByText("Voa Radar")` batia em 4 elementos (header, h1, footer, copyright) — falha de seletor "strict mode violation" do Playwright.
**Solução**: trocado para `getByRole("heading", { name: "Voa Radar" })`, específico o suficiente.

**Problema encontrado ao rodar `npm run test`**: o Vitest tentou executar o spec do Playwright (`tests/e2e/*.spec.ts`) como se fosse um teste seu, porque não havia um `include` explícito — erro de conflito entre os dois test runners.
**Solução**: `vite.config.ts` → `test.include: ['src/**/*.test.ts', 'src/**/*.test.tsx']`, escopando o Vitest só pros testes unitários em `src/`.

**Resultado**: `pytest` (4), Vitest (3) e Playwright E2E (1) passando juntos. Responsividade (desktop 1280px + mobile 390px) e tratamento de erro (testado contra o backend real derrubado, não só lido no código) validados com capturas reais do app, publicadas como artifact pro usuário revisar antes do commit.

**v0.1 considerada funcionalmente fechada** — ver checklist em [ROADMAP.md](../ROADMAP.md). Deploy fica para v0.2, por decisão registrada com o usuário (não fazia parte do escopo original da v0.1 definido no `PROJECT_CONTEXT.md`).
