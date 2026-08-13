# Voa Radar v0.1 — Implementação

> Documento retrospectivo — como a v0.1 foi de fato construída, por etapas. Detalhe de cada decisão em [DECISIONS.md](DECISIONS.md).

## Etapa 1 — Bootstrap

Estrutura de pastas, repositório GitHub próprio (`github.com/RonaldoRhoney/VoaRadar`), padrão RhoneyInc confirmado inspecionando os produtos-irmãos mais recentes (AmaVida, Fit-Now, MenuFlex) antes de propor.

## Etapa 2 — Tela prioritária

Frontend (Vite + React + TS + Tailwind): Home com formulário de orçamento, resultados, detalhe da oportunidade — tudo com mock local no início, identidade visual e rodapé padrão RhoneyInc.

## Etapa 3 — Backend inicial

FastAPI com estrutura simples (`app/config.py`, `app/models/`, `app/routers/`), endpoint `POST /flights/budget-search`, ainda mock, health check.

## Etapa 4 — Governança formal

Adoção de um `CLAUDE.md` detalhado (25 seções) formalizando regras já seguidas informalmente e definindo a arquitetura-alvo do projeto.

## Etapa 5 — Reestruturação para a arquitetura da seção 11

Backend migrado para `app/api/`, `app/core/`, `app/schemas/`, `app/services/`, `app/providers/` (`FlightProvider` abstrato + `MockFlightProvider`). Frontend migrado para `features/budget-search/`, `services/api.ts` (conectando ao backend real), `utils/format.ts`. Código morto (`SearchForm`/`InspireMe`) removido.

## Etapa 6 — Testes

`pytest` (backend), Vitest (frontend), Playwright (E2E) — dois bugs reais encontrados e corrigidos no processo (seletor ambíguo no E2E, conflito entre os dois test runners).

## Etapa 7 — Auditoria completa

Varredura de todos os arquivos do projeto: identidade visual incompleta (favicon genérico, `lang="en"`), código morto do scaffold do Vite, ausência de rota "não encontrada", validação fraca de orçamento no backend. Todos os 7 problemas encontrados foram corrigidos na mesma sessão — ver [../AUDIT_V0.1.md](../AUDIT_V0.1.md).

## Etapa 8 — Fechamento

Commit, tag `v0.1.0`, push.

## Regra seguida

Depois de cada etapa relevante: **Implementado / Testado / Pendente / Riscos / Próximo passo**, sem avançar automaticamente quando havia decisão de produto em aberto (ex: pausas para aprovação antes de cada commit/tag).
