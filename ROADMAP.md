# Roadmap — Voa Radar

Log detalhado de decisões/problemas em [docs/DECISIONS.md](docs/DECISIONS.md).

## Feito

- [x] Estrutura do repositório (`frontend/`, `backend/`, `docs/`) + repo GitHub próprio.
- [x] Frontend: Vite + React + TS + Tailwind, identidade visual e layout responsivo (header/footer padrão RhoneyInc).
- [x] Tela prioritária: busca por orçamento (Home) → lista de destinos dentro do valor → detalhe da oportunidade. Dados mock.
- [x] Backend: FastAPI com estrutura modular, health check, config, endpoint inicial `POST /flights/budget-search` (mock).
- [x] Fluxo ponta a ponta validado no navegador (Playwright headless).

## Próximo (não iniciado, sem decisão de quando)

- [ ] Conectar frontend ao backend real (hoje o frontend usa mock local, não chama a API).
- [ ] Provisionar Supabase dedicado + admin padrão (`rhoneyinc@gmail.com`).
- [ ] Integração com fonte real de dados de voo (Amadeus for Developers, sandbox).
- [ ] Deploy (Vercel) — frontend e backend.
- [ ] Reintroduzir ou remover os componentes de busca clássica (`SearchForm`, `InspireMe`) — hoje existem no código mas não são usados pela Home; decisão pendente do usuário.

## Sugestões futuras registradas (não implementadas)

- Autenticação de usuário / contas / buscas salvas / alertas de preço.
- Deploy do backend FastAPI na Vercel via runtime Python (alternativa a outro host).
