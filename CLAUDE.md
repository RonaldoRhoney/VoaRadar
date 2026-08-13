# Voa Radar — Instruções para Claude Code

> Documentação por versão: os documentos abaixo (PRD, PROJECT_CONTEXT, ROADMAP) descrevem o projeto como um todo. Detalhe de cada versão fica em `docs/v{X.Y}/` — [docs/v0.1/](docs/v0.1/) e [docs/v0.2/](docs/v0.2/), ambos com o mesmo formato (Contexto, PRD, UX, Arquitetura, Implementação, Critérios de aceite, Roadmap, Decisões). A auditoria completa da v0.1 está em [docs/AUDIT_V0.1.md](docs/AUDIT_V0.1.md).

## 1. Identidade do projeto

Você está trabalhando no **Voa Radar**, produto da **RhoneyInc**.

> Nota: a versão deste documento fornecida pelo usuário em 2026-08-12 dizia "Roney Inc." em vez de "RhoneyInc" em uma seção (inconsistente com a própria seção 23 do documento). Sinalizado ao usuário, que confirmou **RhoneyInc** como o nome correto — consistente com o resto do ecossistema (footer, domínio `voaradar.rhoneyinc.com`, demais produtos-irmãos). Resolvido, não é mais um conflito em aberto.

O Voa Radar é uma plataforma de tecnologia voltada à descoberta de oportunidades de viagens aéreas.

### Propósito

Ajudar pessoas a descobrir para onde podem viajar considerando principalmente:

* orçamento disponível;
* local de partida;
* período desejado;
* flexibilidade de datas;
* oportunidades de preços.

A principal proposta do produto é:

> **"Tenho X reais. Para onde posso viajar?"**

O Voa Radar não deve ser tratado simplesmente como um buscador tradicional de passagens. Seu principal diferencial é transformar o orçamento do usuário em possibilidades de viagem.

---

## 2. Regra fundamental

### NÃO CODIFIQUE IMEDIATAMENTE.

Antes de qualquer alteração no projeto:

1. Leia este arquivo.
2. Leia `PROJECT_CONTEXT.md`.
3. Leia `PRD.md`.
4. Leia `ROADMAP.md`.
5. Inspecione a estrutura atual do projeto.
6. Analise o código existente, caso exista.
7. Verifique as tecnologias e dependências existentes.
8. Identifique possíveis problemas.
9. Apresente um plano para a etapa solicitada.
10. Somente implemente depois que a etapa estiver claramente definida.

Nunca assuma que uma funcionalidade deve ser implementada apenas porque parece interessante.

---

## 3. Hierarquia de decisões

Em caso de dúvida, siga esta ordem:

1. Instruções explícitas do usuário.
2. `CLAUDE.md`.
3. `PRD.md`.
4. `PROJECT_CONTEXT.md`.
5. `ARCHITECTURE.md`, quando existir.
6. `ROADMAP.md`.
7. `DECISIONS.md`, quando existir.
8. Código existente.
9. Boas práticas técnicas.

Se houver conflito entre documentos, NÃO escolha silenciosamente. Informe o conflito e peça orientação.

---

## 4. Princípios de desenvolvimento

> **Build small. Validate. Improve.**

Não tentar construir todo o produto de uma vez. Cada etapa deve produzir uma evolução funcional e verificável.

Priorizar: simplicidade, qualidade, manutenção, segurança, acessibilidade, performance, experiência do usuário, arquitetura modular, testes, documentação.

---

## 5. Experiência do usuário

A interface do Voa Radar deve ser: extremamente amigável, intuitiva, moderna, dinâmica, elegante, responsiva, mobile-first, acessível, rápida, visualmente clara.

O usuário deve entender o que fazer sem precisar conhecer termos técnicos de aviação. A interface deve responder visualmente às ações do usuário.

---

## 6. Principal experiência do produto

```text
Usuário
   ↓
Quanto você quer gastar?
   ↓
De onde você quer sair?
   ↓
Quando quer viajar?
   ↓
Não sei para onde ir
   ↓
Encontrar viagens
   ↓
Destinos compatíveis
   ↓
Comparação
   ↓
Detalhes
```

Exemplo:

```text
Orçamento: R$ 800
Origem: Belém
Período: Outubro

Resultado:
Recife       R$ 429
Fortaleza    R$ 517
Brasília     R$ 598
Salvador     R$ 689
```

---

## 7. Primeira fase do desenvolvimento (Etapa 1)

### Frontend

* estrutura React; TypeScript; Vite; Tailwind CSS;
* identidade visual;
* Home;
* formulário principal;
* modo "Não sei para onde ir";
* resultados;
* detalhes da oportunidade;
* responsividade;
* estados de carregamento;
* estados vazios;
* mensagens de erro amigáveis.

### Backend

* Python; FastAPI; estrutura modular; configuração; health check; API inicial;
* arquitetura preparada para integração futura.

### Dados

Na primeira etapa, utilizar dados mockados, claramente identificados internamente como `MOCK DATA`. Nunca apresentar dados fictícios como preços reais.

---

## 8. Não implementar ainda

Durante a primeira fase, NÃO implementar automaticamente: integração real com companhias aéreas, scraping, autenticação completa, pagamentos, IA avançada, previsão de preços, alertas reais, notificações, aplicativo Android, funcionalidades sociais, sistema de afiliados, monetização.

Esses itens pertencem a etapas futuras.

---

## 9. APIs de voos

Arquitetura preparada para múltiplos provedores — não acoplar diretamente a um fornecedor:

```text
FlightProvider
├── AmadeusProvider
├── DuffelProvider
└── FutureProvider
```

Antes de integrar qualquer provedor real, verificar: cobertura, rotas brasileiras, companhias, preços, disponibilidade, limites, documentação, termos de uso, estabilidade.

Nunca afirmar que o sistema pesquisa "todas as companhias" sem comprovação.

---

## 10. Scraping

Não utilizar scraping de sites de companhias aéreas como solução automática. Qualquer necessidade de coleta de dados deve ser analisada considerando: disponibilidade de API, autorização, termos de uso, estabilidade, manutenção, segurança.

---

## 11. Arquitetura

Backend:

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── providers/
│   └── main.py
├── tests/
└── requirements/
```

Frontend:

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── features/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   └── utils/
└── tests/
```

A estrutura poderá ser ajustada caso exista justificativa técnica. Não alterar arquitetura importante sem informar o usuário.

---

## 12. Banco de dados

PostgreSQL quando o banco real for implementado. Entidades previstas: users, airports, airlines, searches, flight_offers, price_history, price_alerts, destinations, providers.

Não criar estruturas complexas antes de serem necessárias.

---

## 13. Segurança

Nunca: colocar API keys no código, colocar secrets no Git, armazenar senhas em texto puro, expor credenciais no frontend, criar endpoints inseguros sem necessidade.

Utilizar variáveis de ambiente. Manter `.env.example` sem valores secretos.

---

## 14. Testes

Toda funcionalidade relevante deverá possuir testes apropriados. Priorizar: testes unitários, testes de integração, testes de API, testes E2E quando fizer sentido.

Não considerar uma funcionalidade concluída apenas porque a interface abre.

---

## 15. Tratamento de erros

Erros devem ser apresentados de forma humana. Nunca mostrar mensagens técnicas cruas (`Internal Server Error`, stack traces). Detalhes técnicos ficam nos logs.

---

## 16. Dados mockados

Mock data é permitido durante desenvolvimento, mas deve estar separado, ser facilmente substituível, não ser confundido com dado real, e não ser usado para mascarar uma integração inexistente.

---

## 17. Regra de não regressão

Ao implementar uma funcionalidade: não quebrar funcionalidades existentes, preservar comportamentos válidos, executar testes, verificar responsividade, verificar console, verificar erros de API. Antes de concluir, realizar uma pequena auditoria da alteração.

---

## 18. Melhorias identificadas

Se identificar uma melhoria fora da tarefa atual, NÃO implementar automaticamente. Registrar como:

```text
Melhoria futura identificada:
Descrição:
Motivo:
Impacto:
Sugestão:
```

E apresentar ao usuário.

---

## 19. Decisões arquiteturais

Não alterar decisões importantes silenciosamente. Antes de mudar framework, banco, arquitetura, estrutura de pastas, estratégia de integração, autenticação ou infraestrutura, explicar: decisão atual, problema identificado, alternativa, vantagem, desvantagem, recomendação. A decisão final pertence ao responsável pelo projeto.

---

## 20. Comunicação

Ao iniciar uma tarefa:

**Entendimento** — o que foi entendido.
**Estado atual** — o que foi encontrado no projeto.
**Plano** — o que se pretende fazer.
**Riscos** — problemas ou decisões importantes.

Depois da implementação:

**Implementado** — o que foi feito.
**Testado** — o que foi validado.
**Pendências** — o que ainda falta.
**Próximo passo sugerido** — o que se recomenda fazer depois.

---

## 21. Regra contra escopo excessivo

Não transformar uma tarefa pequena em uma grande refatoração. Ex.: "Criar a Home" não deve incluir simultaneamente autenticação, banco, alertas, IA, notificações, integração com voos. Manter o foco.

---

## 22. Qualidade visual

Não utilizar interfaces genéricas sem identidade. O Voa Radar deve transmitir: viagem, descoberta, tecnologia, confiança, inteligência, acessibilidade. A interface deve parecer um produto real, não apenas uma demonstração técnica.

---

## 23. RhoneyInc

O Voa Radar é um produto da RhoneyInc. A marca deve aparecer de forma elegante quando apropriado, sem competir visualmente com a marca principal do Voa Radar.

---

## 24. Filosofia

> **"Quanto posso gastar e para onde consigo viajar?"**

A tecnologia deve trabalhar para simplificar essa resposta. Nunca complicar a experiência apenas para demonstrar tecnologia.

---

## 25. Regra final

Antes de qualquer implementação importante, perguntar: isso melhora o produto? Está dentro da etapa atual? Respeita o PRD? Respeita a arquitetura? Melhora a experiência do usuário? Pode ser testado?

Se a resposta for negativa ou incerta, não implementar silenciosamente.

**O objetivo não é escrever o máximo de código possível. O objetivo é construir o Voa Radar corretamente, uma etapa de cada vez.**
