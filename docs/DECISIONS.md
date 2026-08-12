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
