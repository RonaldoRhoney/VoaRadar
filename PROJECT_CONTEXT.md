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
- Deploy: Vercel (projeto próprio).
- Dados/Auth: Supabase dedicado (a provisionar).
- Rodapé, admin padrão e demais convenções: skills `footer-padrao` e `admin-padrao` do ecossistema.

## Origem e propósito

O Voa Radar nasceu da ideia de ajudar pessoas a encontrar passagens aéreas mais acessíveis — não como produto pensado primeiro pra gerar receita, mas como ferramenta útil, projeto tecnológico relevante e demonstração de capacidade profissional (também é peça de portfólio técnico: Python, FastAPI, React, TypeScript, PostgreSQL, arquitetura, testes, CI/CD, IA, mobile).

Propósito social: mostrar que viajar de avião pode estar mais acessível do que muita gente imagina, ajudando a descobrir possibilidades, comparar opções e tomar decisões melhores — sem prometer cobertura que não existe.

Posicionamento: **"Seu radar para viajar pagando menos."**

## Visão de evolução

- **v0.1** — Fundação + interface + busca com mock data (fase atual).
- **v0.2** — Explorar destinos.
- **v0.3** — Histórico e análise de preços.
- **v0.4** — Alertas.
- **v0.5** — Inteligência (IA).
- **v1.0** — Plataforma pública.
- **Futuro** — PWA e Android nativo.

Regra de desenvolvimento: **Entender → Planejar → Implementar → Testar → Validar → Evoluir** — nunca "imaginar → codificar tudo → corrigir depois".

## O que o projeto não deve fazer

Vender diretamente passagens no MVP; fingir que possui dados reais quando não possui; prometer cobertura total sem comprovação; depender obrigatoriamente de uma única API de voo; usar scraping indiscriminadamente; implementar funcionalidades só para aumentar o tamanho do projeto.

## Estado atual

MVP visual da tela principal (orçamento → destinos → oportunidade) construído com **dados mock**, tanto no frontend quanto no backend — claramente marcados como tal no código (`MOCK DATA` / `MockFlightProvider`). Nenhuma integração com fonte real de dados de voo ainda. Detalhe completo e atualizado em [ROADMAP.md](ROADMAP.md) e [docs/v0.1/DECISIONS.md](docs/v0.1/DECISIONS.md).
