# Contexto do projeto — Voa Radar

## O que é

Voa Radar é um buscador/plataforma de passagens aéreas. Produto da RhoneyInc, usado também como projeto de portfólio — por isso arquitetura, decisões e problemas são documentados ao longo da construção, não só o resultado final (ver [docs/v0.1/DECISIONS.md](docs/v0.1/DECISIONS.md), [docs/v0.2/DECISIONS.md](docs/v0.2/DECISIONS.md) e [ROADMAP.md](ROADMAP.md)).

## Público

Pessoas planejando viagem que querem comparar preços de voos rapidamente — incluindo quem ainda não decidiu o destino, só o quanto quer gastar.

## Diferencial de produto

A experiência de entrada não é "origem + destino + data" (padrão de mercado). É **orçamento-primeiro**: o usuário diz quanto quer gastar, de onde sai e quando, e o Voa Radar sugere destinos que cabem nesse orçamento — com a opção de já buscar por um destino específico ficando em segundo plano.

## Padrão RhoneyInc seguido

- Frontend: React + TypeScript + Vite + Tailwind.
- Backend: API própria (FastAPI), estrutura modular.
- Deploy: Vercel (projeto próprio, a fazer).
- Dados/Auth: Supabase dedicado — entra na v0.3 (ver [docs/v0.3/DECISIONS.md](docs/v0.3/DECISIONS.md) DEC-013).
- Rodapé, admin padrão e demais convenções: skills `footer-padrao` e `admin-padrao` do ecossistema.

## Origem e propósito

O Voa Radar nasceu da ideia de ajudar pessoas a encontrar passagens aéreas mais acessíveis — não como produto pensado primeiro pra gerar receita, mas como ferramenta útil, projeto tecnológico relevante e demonstração de capacidade profissional (também é peça de portfólio técnico: Python, FastAPI, React, TypeScript, PostgreSQL, arquitetura, testes, CI/CD, IA, mobile).

Propósito social: mostrar que viajar de avião pode estar mais acessível do que muita gente imagina, ajudando a descobrir possibilidades, comparar opções e tomar decisões melhores — sem prometer cobertura que não existe.

Posicionamento: **"Seu radar para viajar pagando menos."**

## Visão de evolução

- **v0.1** — Fundação + interface + busca com mock data. ✅ Concluída (tag `v0.1.0`).
- **v0.2** — Explorar destinos (múltiplas ofertas, filtros, ordenação). ✅ Concluída (tag `v0.2.0`).
- **v0.3** — Price Intelligence: histórico e análise de preços, Postgres via Supabase. 🚧 Em fechamento (fase atual) — schema, coleta, motor de análise, API e frontend prontos e validados contra dado real.
- **v0.4** — Radar / Alertas.
- **v0.5** — Inteligência (IA/recomendações).
- **v1.0** — Plataforma pública.
- **Futuro** — PWA e Android nativo.

Regra de desenvolvimento: **Entender → Planejar → Implementar → Testar → Validar → Evoluir** — nunca "imaginar → codificar tudo → corrigir depois".

## O que o projeto não deve fazer

Vender diretamente passagens no MVP; fingir que possui dados reais quando não possui; prometer cobertura total sem comprovação; depender obrigatoriamente de uma única API de voo; usar scraping indiscriminadamente; implementar funcionalidades só para aumentar o tamanho do projeto.

## Estado atual

v0.1 e v0.2 concluídas: exploração de destinos por orçamento, múltiplas ofertas por destino, filtros e ordenação, tudo com **dados mock** (frontend e backend), claramente marcados como tal no código (`MOCK DATA` / `MockFlightProvider`). Nenhuma integração com fonte real de dados de voo ainda.

v0.3 fechada: Supabase (Postgres) conectado e populado com histórico de exemplo; motor de Price Intelligence (mínimo/máximo/média/mediana/score/confiança, estatística transparente, sem fabricar inteligência) funcionando de ponta a ponta — API (`GET /flights/price-intelligence/{offer_id}`) e frontend (badge de oportunidade, explicação, gráfico de histórico) validados contra dado real no Supabase.

v0.4 fechada: Radar & Alertas (monitoramento de rota, disparo por regra, central de notificações, auth real via Supabase) — tag `v0.4.0`. Extensão pós-release em andamento: Admin padrão (só FASE A concluída até agora).

**"RhoneyInc Zero-Cost API First" (2026-08-16)**: nenhuma fonte externa entra em produção com risco de cobrança automática (skill `zero-cost-api`, `MyApps/.claude/skills/`). `MockFlightProvider` continua sendo o único provider de oferta comprável — nenhuma integração real de companhia aérea existe ainda. ANAC (dados abertos, gratuita) está projetada como fonte de referência histórica (não oferta), aguardando aprovação de implementação. Ver `docs/DATA_SOURCES.md`/`PROVIDER_ARCHITECTURE.md`.

Detalhe completo em [ROADMAP.md](ROADMAP.md), [docs/v0.1/](docs/v0.1/), [docs/v0.2/](docs/v0.2/), [docs/v0.3/](docs/v0.3/) e [docs/v0.4/](docs/v0.4/).
