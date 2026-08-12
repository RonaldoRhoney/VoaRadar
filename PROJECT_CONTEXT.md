# Contexto do projeto — Voa Radar

## O que é

Voa Radar é um buscador/plataforma de passagens aéreas. Produto da RhoneyInc, usado também como projeto de portfólio — por isso arquitetura, decisões e problemas são documentados ao longo da construção, não só o resultado final (ver [docs/DECISIONS.md](docs/DECISIONS.md) e [ROADMAP.md](ROADMAP.md)).

## Público

Pessoas planejando viagem que querem comparar preços de voos rapidamente — incluindo quem ainda não decidiu o destino, só o quanto quer gastar.

## Diferencial de produto

A experiência de entrada não é "origem + destino + data" (padrão de mercado). É **orçamento-primeiro**: o usuário diz quanto quer gastar, de onde sai e quando, e o Voa Radar sugere destinos que cabem nesse orçamento — com a opção de já buscar por um destino específico ficando em segundo plano.

## Padrão RhoneyInc seguido

- Frontend: React + TypeScript + Vite + Tailwind.
- Backend: API própria (FastAPI), estrutura modular.
- Deploy: Vercel (projeto próprio).
- Dados/Auth: Supabase dedicado (a provisionar).
- Rodapé, admin padrão e demais convenções: skills `footer-padrao` e `admin-padrao` do ecossistema.

## Estado atual

MVP visual da tela principal (orçamento → destinos → oportunidade) construído com **dados mock**, tanto no frontend quanto no backend — claramente marcados como tal no código (`MOCK DATA` / `budgetDestinationsMock`). Nenhuma integração com fonte real de dados de voo ainda.
