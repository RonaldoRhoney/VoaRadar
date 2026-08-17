# Voa Radar v0.4 — Decisões

## DEC-100 — Conceito de produto é "Radar", nunca "Alerta"

Decisão de identidade, não só nomenclatura técnica. Toda a interface, API e documentação usam "Radar" ("Meu Radar Recife", "Criar Radar", "Radar ativo"). Origem: proposta do usuário no planejamento da v0.4 (`docs/v0.4/v0.4.txt`).

## DEC-101 — Autenticação vira requisito da v0.4, não funcionalidade isolada

Um Radar pertence a um usuário; sem dono, "Meus Radares" não existe e a RLS auditada na v0.3 não tem o que proteger de forma diferenciada. Auth mínima (cadastro, login, logout, sessão, recuperação de senha) entra como pré-requisito estrutural, não como extra. Escopo deliberadamente pequeno — sem OAuth social, sem 2FA.

**Confirmado pelo usuário**: método de auth = e-mail + senha (não link mágico).

## DEC-102 — `condition_type` como colunas em `radars`, não tabela `radar_conditions`

A v0.4.0 só suporta uma condição por Radar. Modelar como tabela separada agora seria complexidade sem função imediata (join sem necessidade). Revisar quando/se condições combinadas forem pedidas.

**Implica**: "avisar abaixo de um valor fixo" e "avisar abaixo do meu orçamento" foram fundidos num único `condition_type = PRICE_BELOW` — do ponto de vista do motor são a mesma operação (comparar preço com um número). Proposto na análise arquitetural e não houve objeção — adotado como decisão, sinalizado aqui explicitamente para poder ser revertido se o usuário discordar depois de ver a implementação.

## DEC-103 — Cooldown de deduplicação: 24h ou queda de 5%

**Confirmado pelo usuário** entre as opções apresentadas. Um Radar não gera nova notificação para a mesma oportunidade dentro de 24h, a menos que o novo preço seja pelo menos 5% menor que o do último evento notificado. Detalhe em `ALERT_RULES.md` §2. Ajustável com dado de uso real — não é considerado definitivo/imutável.

## DEC-104 — Nenhum worker/scheduler novo na v0.4.0

Avaliação de Radar é orientada a evento, acoplada ao mesmo ponto que já persiste uma nova `price_snapshot` (`record_observation`, v0.3). Motivo: não existe hoje coleta automática contínua de preços reais — um scheduler não teria o que verificar de forma independente da própria coleta, que ainda é manual/simulada (`scripts/seed_history.py`). Reavaliar quando a integração real de provedor (v0.5+) definir uma cadência própria de coleta.

**Risco aceito e registrado**: se um dia uma `price_snapshot` for gravada por um caminho de código diferente de `record_observation`, o Radar Engine não é acionado para ela. Precisa virar teste de integração explícito na FASE 8, não ficar como suposição implícita.

## DEC-105 — RLS com policy condicional real, não mais "negar tudo"

Diferente do padrão da v0.3 (DEC-021: RLS habilitado mas `anon`/`authenticated` sem nenhum acesso), as tabelas da v0.4 (`radars`, `radar_events`, `notifications`) precisam de policy real (`auth.uid() = user_id`) porque `authenticated` passa a ter uso legítimo. RLS funciona como segunda camada — o backend continua conectando com role que faz bypass, e a query do repository é a primeira linha de defesa de isolamento (`SECURITY.md` §2).

## DEC-106 — 404 (não 403) em acesso cross-user

Consistente com prática de segurança padrão: 403 confirmaria a existência do recurso para quem não é dono, vazando informação. Proposto na análise arquitetural, sem objeção do usuário — adotado.

## DEC-107 — `profiles` fica mínimo (só `id` + `created_at`)

Nenhum campo além do estritamente necessário pra existir uma linha vinculada a `auth.users`. Proposto sem objeção — adotado. Adicionar campos (nome, avatar) apenas sob demanda real de uma tela futura, não especulativamente (princípio já usado no resto do projeto).

## DEC-108 — "Qualquer destino" fora do release inicial

`destination_airport_id` é obrigatório em `radars` na v0.4.0. Motivo: "qualquer destino" multiplica o espaço de rotas avaliadas pelo motor a cada snapshot, e só faz sentido com estratégia de coleta em escala já definida — hoje não existe. Fica para v0.4.x, com passo intermediário "origem → região" antes de "qualquer destino" irrestrito.

## DEC-109 — Sempre `REVOKE ALL` antes de `GRANT`, nunca só `GRANT`

Achado real na FASE 5 (não hipotético): as migrations `0004`-`0007` concediam grants seletivos a `authenticated` sem antes revogar tudo — e o Supabase já tinha concedido automaticamente `INSERT/UPDATE/DELETE/TRUNCATE/REFERENCES/TRIGGER` a `authenticated` em toda tabela nova do schema `public` (comportamento padrão de projeto, via `ALTER DEFAULT PRIVILEGES`). Como `GRANT` é aditivo, o grant automático continuou valendo por baixo do `GRANT` seletivo da migration — `profiles`, pensada como somente leitura, ficou com acesso de escrita/exclusão completo pra `authenticated`.

**Correção**: migration `0008`. **Regra daqui pra frente**: toda migration que cria tabela no `public` faz `REVOKE ALL ON TABLE <t> FROM anon, authenticated` **antes** de qualquer `GRANT`, mesmo que a intenção seja conceder algo depois — nunca assumir que a tabela nasce sem acesso. Ver `SECURITY.md` §6.

## DEC-110 — Frontend fala com o backend pra auth, não direto com o Supabase Auth (revisa ARCHITECTURE.md §3/§7)

`ARCHITECTURE.md` previa o frontend usando o SDK `@supabase/supabase-js` diretamente pra sessão/login, com refresh automático. Na implementação (FASE 6), optei por manter tudo passando pelos endpoints já construídos e testados na FASE 5 (`POST /auth/signup`, `/auth/login`, `/auth/logout`), com o frontend guardando `access_token`/`refresh_token` em `localStorage`.

**Motivo**: o backend já cria a linha em `profiles` de forma atômica com o cadastro (`api/auth.py`); usar o SDK do Supabase direto no frontend exigiria ou duplicar essa lógica (profile criado por outro caminho, ex: trigger de banco) ou um endpoint extra só pra "confirmar profile depois do signup" — mais uma peça móvel sem benefício claro nesta fase. Evita também manter configuração do Supabase (URL, anon key) duplicada em dois `.env` (backend e frontend).

**Custo aceito**: sem refresh automático de sessão nesta versão — o `access_token` expira (padrão do Supabase, ~1h) e o usuário precisa logar de novo. Registrado como limitação conhecida da v0.4.0, não como lacuna esquecida — refresh automático via `refresh_token` é candidato natural pra v0.4.x se o atrito for sentido no uso real.

## DEC-111 — Validação de JWT via JWKS/ES256, não HS256 com segredo fixo

Achado real ao configurar as chaves de verdade (2026-08-14): `SECURITY.md`/`ARCHITECTURE.md` previam validar o JWT do Supabase Auth com um `SUPABASE_JWT_SECRET` (HS256, segredo compartilhado). Ao abrir o painel do projeto (Settings > JWT Keys), o Supabase já tinha migrado esse projeto pras chaves assimétricas novas (ECC P-256/ES256) — a `Legacy JWT Secret` aparecia só como chave anterior, rotacionada 2 dias antes, válida só pra tokens já emitidos (que expiram em ~1h e já tinham expirado).

**Correção**: `core/auth.py` passou a buscar as chaves públicas de assinatura no endpoint JWKS do próprio Supabase (`/auth/v1/.well-known/jwks.json`), cacheado em memória por 1h, casando o token pelo `kid` do header e validando com o algoritmo declarado (`ES256`). `SUPABASE_JWT_SECRET` foi removido de `Settings`/`.env`/`.env.example` — não existe mais no fluxo. Testado: 88/88 pytest (com par de chaves EC gerado em `conftest.py` e `get_jwks` sobrescrito via `dependency_overrides`, mesmo padrão de `get_db`) e validado ao vivo contra o Supabase real (cadastro → confirmação manual do e-mail de teste → login → token ES256 real validado pelo backend → `GET /radars` autenticado retornando 200).

**Lição**: a documentação (`SECURITY.md`, `ARCHITECTURE.md`) foi escrita antes de olhar o painel real do projeto — o modelo de auth do Supabase mudou de HS256 pra ES256/JWKS como padrão em projetos novos, e a doc não podia saber disso sem verificar. Reforça `verificar-premissas` (skill RhoneyInc): specs escritas antes de olhar o painel/API real de um provedor terceiro são hipótese, não fato, até confirmar.

## DEC-112 — `ON DELETE CASCADE` de `radars` para `radar_events`/`notifications`

Achado real ao testar `DELETE /radars/{id}` ao vivo contra o Supabase (2026-08-14): as migrations `0005`-`0007` não declararam `ondelete="CASCADE"` nas FKs de `radar_id`/`radar_event_id`. Um Radar que já tinha disparado pelo menos uma vez (tinha `radar_events`/`notifications` associados) não podia ser apagado — `IntegrityError` cru, que viraria um 500 sem tratamento pro usuário (a API não tinha (nem devia ter) um `try/except IntegrityError` específico pra esse caso; a correção certa é o schema permitir a operação, não capturar o erro depois).

**Correção**: migration `0009` — `ON DELETE CASCADE` em `radar_events.radar_id`, `notifications.radar_id` e `notifications.radar_event_id`. Um Radar é dono do seu log de eventos e das notificações que gerou; apagar o Radar apaga os dois junto, não deixa órfão nem bloqueia a exclusão. Models atualizados pra declarar o mesmo `ondelete` (documentação viva do schema real).

**Lição de teste**: o teste automatizado original não pegou esse bug porque o SQLite dos testes não aplica `PRAGMA foreign_keys=ON` por padrão — FKs eram silenciosamente ignoradas, então até uma migration com FK errada "passava". Corrigido em `conftest.py` (liga o pragma na conexão de teste) — agora o SQLite se comporta como o Postgres real nesse aspecto, consistente com a filosofia de portabilidade já registrada em `docs/v0.3/DECISIONS.md` DEC-014.

## DEC-113 — Notificações viram um `NotificationsProvider` (estado compartilhado), não um hook independente por componente

Achado de revisão manual (2026-08-14): `Header.tsx` (sino) e `pages/Notifications.tsx` chamavam `useNotifications` cada um com sua própria instância — marcar uma notificação como lida numa tela não atualizava a contagem na outra até recarregar a página.

**Correção**: `features/notifications/NotificationsProvider.tsx`, mesmo padrão do `AuthProvider` — uma única fonte de verdade montada em `main.tsx`, envolvendo `<App />`. `useNotifications()` deixou de receber `accessToken` como parâmetro (lê a sessão internamente via `useAuth`).

## DEC-114 — `PUT /radars/{id}` valida a condição no estado final mesclado, não no corpo da requisição

Achado de revisão manual: `RadarCreate` tem um `model_validator` garantindo que `condition_type=PRICE_BELOW` sempre venha com `condition_price` (e o mesmo pra `OPPORTUNITY_CLASSIFICATION`/`condition_classification`). `RadarUpdate` é parcial (`exclude_unset`) e não pode ter a mesma validação por campo isolado — um PATCH que só manda `condition_type` novo, sem o campo de valor correspondente, passava pelo schema e salvava um Radar que nunca dispararia, em silêncio.

**Correção**: `api/radars.py` valida o objeto `radar` já mesclado (depois do `setattr`, antes do `commit`) e responde 422 amigável se a combinação ficar inconsistente. Também limpa o campo da condição anterior ao trocar de tipo (`condition_classification=None` ao virar `PRICE_BELOW`, e vice-versa) — higiene de dado, evita lixo que nenhuma leitura usa mais.

## DEC-115 — `radars` ganha o mesmo CHECK de `routes`: origem ≠ destino

Achado de revisão manual: `routes` tem `CHECK (origin_airport_id != destination_airport_id)` desde a v0.3 (`0001`); `radars` referencia aeroportos diretamente (não `routes`, ver `DATA_MODEL.md` §6) e não tinha a mesma garantia — nada impedia criar um Radar com origem igual ao destino (inofensivo, mas nonsense de produto: nunca existiria rota real pra casar).

**Correção em 3 camadas**: `RadarCreate.model_validator` (schema), validação do estado final mesclado no `PUT` (mesmo mecanismo do DEC-114), e `CHECK` constraint no banco (migration `0010`, defesa em profundidade — mesmo princípio já estabelecido pra RLS).

## DEC-116 — Admin via skill `admin-padrao`: trigger no banco, não lógica no backend

Pedido explícito do usuário (2026-08-14): `rhoneyinc@gmail.com` vira admin do Voa Radar, com painel próprio (fora do escopo original da v0.4 — item registrado antes como "melhoria futura", agora implementado). Aplica a skill RhoneyInc `admin-padrao` (`.claude/skills/admin-padrao/SKILL.md`).

**Por que trigger em `auth.users`, não código no `/auth/signup`**: o login social (Google, FASE C planejada) cria a linha em `auth.users` direto pelo Supabase Auth, sem nunca chamar o backend — qualquer lógica de promoção que vivesse só no endpoint de signup do backend nunca rodaria pra cadastro via Google. Um trigger `handle_new_user()` (migration `0011`, `SECURITY DEFINER`) cobre os dois caminhos de uma vez, mesma referência já usada no hub RhoneyInc.

`profiles.role` (`user`/`admin`, default `user`) + `CHECK` constraint. `GET /auth/me` devolve `{id, email, role}` a partir do JWT validado + leitura de `profiles` — o frontend nunca decide/guarda isso sozinho, só reage ao que o backend confirma (mesmo princípio de `SECURITY.md` §2).

**Validado ao vivo**: migration aplicada no Supabase real, trigger e função `SECURITY DEFINER` confirmados via `pg_trigger`/`pg_proc`; cadastro real de teste (e-mail diferente de `rhoneyinc@gmail.com`) confirmou `role='user'` atribuído automaticamente pelo trigger — mesma lógica que atribui `role='admin'` na correspondência exata do e-mail. Não criei a conta `rhoneyinc@gmail.com` de verdade nesta sessão (é a conta real do usuário — ele deve criá-la pelo fluxo normal de cadastro, com a senha que escolher).

## DEC-117 — "RhoneyInc Zero-Cost API First": discovery de providers, nenhuma implementação ainda

Pedido do usuário (2026-08-16): formalizar "custo R$ 0" como restrição arquitetural, não preferência, e avaliar `FlightProvider` real (Amadeus, OpenSky, Aviationstack, ANAC) antes de qualquer código. Nova skill institucional RhoneyInc criada: `MyApps/.claude/skills/zero-cost-api/SKILL.md`.

**Verificação real corrigiu 2 premissas da proposta original antes de desenhar arquitetura**: Amadeus Self-Service (o "ambiente de teste gratuito" proposto) foi **descontinuado de vez em 17/jul/2026** — confirmado por múltiplas fontes independentes (PhocusWire, LinkedIn, TravelTrade), não é mais uma opção, nem em teste. OpenSky Network e Aviationstack são APIs reais e gratuitas, mas **nenhuma das duas fornece preço de passagem** — só rastreamento de posição (OpenSky, ADS-B) e status/horário de voo (Aviationstack), respectivamente; OpenSky também restringe uso a não-comercial. Das 4 fontes avaliadas, só a **ANAC** (dados abertos, download CSV direto do site oficial, sem token) sobrou como viável — e mesmo essa só como referência histórica mensal, nunca oferta comprável em tempo real (papel que a proposta original já reservava corretamente pra ela).

**Distinção arquitetural registrada**: `FlightProvider` (interface já existente desde v0.1, `base.py`) é pra oferta comprável — `MockFlightProvider` continua sendo o único implementado. ANAC vira um componente **diferente**, `FareReferenceProvider` (proposto, não implementado), porque misturar "oferta" com "média histórica" na mesma interface seria enganoso pro usuário.

**Documentos criados** (`docs/DATA_SOURCES.md`, `docs/API_LIMITS.md`, `docs/LICENSES.md`, `docs/PROVIDER_ARCHITECTURE.md`) — nenhuma linha de código alterada, aguardando aprovação explícita antes de implementar `AnacFareProvider`/tabela `anac_fare_reference`/integração no Price Intelligence.

**Correção de comunicação registrada**: nunca prometer "consulta Azul/GOL/LATAM diretamente" — nenhuma integração com companhia aérea existe ou está planejada. Comunicação correta: "combina fontes públicas e provedores de dados de aviação".

## DEC-118 — `AnacFareProvider` implementado (PA.1-PA.4) e primeiro deploy de produção do Voa Radar

Pedido do usuário (2026-08-16): "implemente" (autorização explícita do plano do DEC-117) seguido de "faça o deploy".

**Implementado**: `AnacFareProvider`/`FareReferenceProvider` (`app/providers/`), repositório `AnacFareRepository`, modelo `AnacFareReference` e migration `0012` (tabela `anac_fare_reference`, RLS habilitada, sem grants para `anon`/`authenticated` — mesmo padrão de `price_history`). `PriceIntelligenceService` ganhou `fare_reference_provider` opcional; ausência da fonte nunca quebra a resposta (`anac_reference: null`), só omite o campo. Endpoint `/flights/price-intelligence/{offer_id}` já injeta o provider real.

**Não implementado ainda, deliberadamente**: `scripts/import_anac_fares.py`. O schema real do CSV da ANAC não foi verificado — o download de tarifas está atrás de uma ferramenta de consulta interativa no site oficial, não um link estático, e o acesso direto ao domínio `anac.gov.br` falhou a partir do sandbox. Nomes de coluna usados em qualquer rascunho anterior (EMPRESA/ANO/MES etc.) eram suposição de busca genérica, não confirmados contra um arquivo real — não seriam implementados sem essa verificação, por princípio (`CLAUDE.md` §2). Pendente: usuário baixar uma amostra real do CSV, ou investigar o mecanismo de exportação da ferramenta interativa.

**Testado**: 94/94 testes passando (nenhuma regressão). Validado ao vivo em produção via `/flights/price-intelligence/offer-rec-001?price=429` — campo `anac_reference: null` presente e correto (nenhuma rota tem referência ANAC importada ainda, comportamento esperado).

**Primeiro deploy de produção do Voa Radar** (frontend + backend), na Vercel:
- Backend (`voaradar-api`): `@vercel/python`, entrypoint `backend/api/index.py` expondo o mesmo app FastAPI de sempre. `requirements.txt` precisou ser uma lista flat de pacotes — a Vercel não suporta a diretiva `-r requirements/base.txt` usada localmente ("could not parse requirements.txt"). 5 env vars de produção configuradas (`DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `ENVIRONMENT`, `CORS_ORIGINS`).
- Frontend (`voaradar-frontend`): build Vite padrão, env var `VITE_API_BASE_URL` apontando pro backend real.
- **Gotcha novo pro padrão RhoneyInc**: projetos novos na Vercel nascem com "Deployment Protection" (SSO) ativado por padrão em `*.vercel.app`, retornando 302 (redirect pro login Vercel) em vez de servir o conteúdo — mesmo com env vars e build corretos. Corrigido via `PATCH https://api.vercel.com/v9/projects/{id}?teamId={team}` com `{"ssoProtection": null}` (não existe toggle direto no `vercel.json`). Necessário em ambos os projetos (backend e frontend). Vale registrar como passo do checklist "novo app no ar" pra não repetir o diagnóstico do zero da próxima vez.
- CORS do backend liberado explicitamente para os domínios estáveis do frontend (`voaradar-frontend-ronaldorhoneys-projects.vercel.app` e o alias curto `frontend-seven-theta-82.vercel.app`), verificado via `OPTIONS` com header `Origin` real — `access-control-allow-origin` correto.

**Pendente**: domínio próprio `voaradar.rhoneyinc.com` (hoje só existem URLs `*.vercel.app` padrão), entrada no hub RhoneyInc e nos rodapés dos produtos-irmãos.

## DEC-119 — Voa Radar publicado nos padrões RhoneyInc (skill `novo-app-no-ar`)

Pedido do usuário (2026-08-16): "publique o VoaRadar com os mesmo padrões RhoneyInc". Aplicado o checklist da skill institucional `novo-app-no-ar`:

- **Domínio**: `voaradar.rhoneyinc.com` criado via `vercel domains add` apontando pro projeto `voaradar-frontend` — confirmado ao vivo (HTTP 200), sem precisar mexer em DNS externo (o domínio `rhoneyinc.com` já é registrado no próprio Vercel).
- **Ícone**: `RhoneyInc/assets/voaradar-icon.svg` criado seguindo o padrão dos demais produtos (mesma estrutura de `vagalume-icon.svg`), cor de acento `#34E0A1` (o verde já usado no produto, `--color-radar-400`).
- **Registro em `softwares`** (tabela do hub RhoneyInc, Supabase `crkryabvsmlraizaurnk`): inserido com `status='em_desenvolvimento'` — decisão consciente, não "no ar" = "pronto pro público" (mesmo princípio já aplicado ao AmaVida/KnowRa/MontaMovel): hoje o Voa Radar só tem `MockFlightProvider` (dado fictício, nunca preço real) e o admin (FASE B/C) ainda não foi implementado. `ordem=10`, `link_url` e `logo_url` apontando pro domínio e ícone reais.
- **Rodapé do hub**: link adicionado em `RhoneyInc/index.html` (coluna "Produtos"), apontando direto pro domínio do produto (não existe uma página `voaradar.html` de marketing dentro do site RhoneyInc, diferente dos demais — ver "melhoria futura" abaixo).
- **Rodapé do próprio produto**: já seguia a skill `footer-padrao` desde antes, nenhuma correção necessária.
- Hub redeployado (`vercel --prod` em `RhoneyInc/`, padrão do projeto — não é push-triggered) e verificado ao vivo: link "Voa Radar" presente no HTML servido em produção.

**Melhoria futura identificada** (não implementada, fora de escopo desta tarefa): os demais produtos têm uma página de marketing dedicada dentro do próprio site RhoneyInc (`vagalume.html`, `amavida.html` etc., usada nos cards "Saiba mais →" de uma seção estática mais antiga da home, separada do carrossel dinâmico) — o Voa Radar não tem equivalente. Também faltam `privacidade.html`/`termos.html`/`contato.html` no próprio `voaradar.rhoneyinc.com` (retornam 404 hoje), presentes em todos os produtos-irmãos já publicados. Ambos exigem conteúdo específico (copy de marketing, texto LGPD) que não deveria ser escrito silenciosamente — registrado aqui para decisão explícita do usuário.

## Pendência herdada da v0.3 — resolvida

Tag `v0.3.1` cortada em 2026-08-14 (commit `4ce0d72`), cobrindo os 2 commits de segurança pós-`v0.3.0` (`b36e624`, `a7c698b`) + o E2E que faltava. Ver `docs/v0.3/ACCEPTANCE.md`.

## DEC-120 — Admin FASE C: login social Google habilitado (2026-08-17)

Pedido do usuário: "vamos habilitar login com google" — completa a FASE C mencionada em DEC-116 (Admin padrão), que até aqui só tinha a FASE A (`profiles.role` + trigger) concluída.

**Arquitetura**: o backend já validava qualquer JWT emitido pelo Supabase Auth via JWKS (`app/core/auth.py`), provider-agnostic desde sempre — login social não exigiu nenhuma mudança no backend. Só o frontend precisou de: `features/auth/oauth.ts` (redireciona o navegador pro fluxo OAuth do Supabase, sem depender de `supabase-js` — mantém a arquitetura existente de auth via backend REST, só o redirect inicial e o parse do retorno acontecem client-side, que é inerente ao fluxo OAuth de página inteira), nova página `AuthCallback` (lê o token do fragmento da URL, nunca da query string — não vai pro histórico nem pra log de servidor), e botão "Continuar com Google" em `Login`/`Signup`.

**Google OAuth Client "VoaRadar Supabase"** criado pelo usuário no projeto Google Cloud `meupet-501512` (mesmo projeto de MeuPet/KnowRa/FinTra, cada produto com seu próprio Client ID — confirma o padrão já documentado na memória RhoneyInc). Callback `https://ehdjptcyhzszglrlvpjz.supabase.co/auth/v1/callback` autorizado no Google. Auth do Supabase (Site URL, redirect URLs, provider Google) configurado via Management API com um Personal Access Token gerado pelo usuário — mesmo fluxo do FinTra, nenhum clique manual no dashboard do Supabase além de gerar o token.

**Gotcha de segurança recorrente, corrigido de novo**: um `client_secret_*.json` baixado do Google Cloud Console apareceu na raiz do repo durante a configuração — removido do disco antes de qualquer commit, `client_secret_*.json` adicionado ao `.gitignore` (mesmo achado do FinTra DEC-001 — vale registrar como passo permanente do checklist de qualquer produto RhoneyInc que configure Google OAuth).

**Testado ao vivo em produção**: `GET /auth/v1/authorize?provider=google` redireciona corretamente pro Google com o `client_id` certo e `redirect_uri` apontando pro callback do Supabase do VoaRadar. Build, 16/16 testes de frontend e lint continuam limpos.

Deploy de produção do frontend atualizado (`voaradar.rhoneyinc.com`), com `VITE_SUPABASE_URL` configurada.

**Bug real encontrado pelo usuário após o login de verdade**: `/auth/callback` devolvia 404 puro da Vercel (`NOT_FOUND`) em vez de carregar o app. Causa: o frontend nunca tinha `vercel.json` — a Vercel serve arquivo estático por padrão, e uma navegação de página inteira (o redirect do Google/Supabase, não navegação client-side do React Router) pra uma rota que só existe no React Router não encontra arquivo físico correspondente. Corrigido com `frontend/vercel.json` (`rewrites` redirecionando qualquer path pro `index.html`, deixando o React Router assumir depois que a SPA carrega) — o fragmento `#access_token=...` da URL é preservado pelo navegador independente do rewrite do servidor, então o `AuthCallback` continua lendo o token corretamente. Re-testado: `/auth/callback`, `/radares` e `/` retornam 200. Vale registrar no checklist "novo app no ar": toda SPA da RhoneyInc no Vercel precisa desse rewrite desde o primeiro deploy, não só quando uma rota client-side quebra.

## DEC-121 — Admin FASE B: painel de métricas (2026-08-17)

Pedido do usuário: "pode seguir o fluxo" — próximo item pendente da extensão Admin (FASE A e FASE C já concluídas), sem plano detalhado registrado ainda, então montei um a partir do modelo de dado existente (`profiles`, `radars`, `radar_events`, `notifications`) antes de codificar.

**Backend**: `app/api/admin.py`, endpoint `GET /admin/metrics`, protegido por `require_admin` (decide o `role` só a partir de `profiles`, nunca de claim do token — mesmo princípio de `/auth/me`). Métricas **só agregadas** (`PlatformMetrics`): usuários totais, radares totais/ativos, oportunidades detectadas (`radar_events`), notificações enviadas, novos usuários/radares nos últimos 7 dias — nunca expõe qual rota ou preço um usuário específico está monitorando (mesmo cuidado de minimização já aplicado no painel admin do FinTra, DEC-002).

**Frontend**: `/admin` (nova rota, `AdminPanel.tsx`), protegida por `AdminRoute` — que espera o `role` carregar (`roleLoading`) antes de decidir redirecionar, pra não expulsar um admin de verdade só porque a checagem assíncrona ainda não voltou. Link "Painel Admin" no header, visível só quando `role === "admin"`. `AuthContext` ganhou `role`/`roleLoading`, buscado via `/auth/me` sempre que a sessão muda (login, cadastro, callback do Google).

**Testado**:
- 3 testes novos de backend (`tests/test_admin_api.py`): sem token → 401, usuário comum → 403, admin → 200 com contagens corretas. 97/97 testes de backend passando, Bandit limpo.
- **Ao vivo em produção**: criado usuário de teste real (e removido depois), confirmado 403 como usuário comum, promovido a admin direto no banco, confirmado 200 com `total_users`/`new_users_7d` corretos batendo com o estado real do banco.
- Build, 16/16 testes de frontend e lint continuam limpos. `/admin` retorna 200 em produção.

Fecha a extensão Admin padrão (FASE A + B + C completas).

**Bug real encontrado pelo usuário logo depois ("não funcionou", não conseguia acessar `/admin`)**: condição de corrida no `AdminRoute`. `roleLoading` iniciava sempre `false` — no primeiro render de uma navegação direta pra `/admin` com uma sessão já salva (o caso normal, não um login novo), o `AdminRoute` via `session` presente + `roleLoading=false` + `role=null` (ainda não buscado) e interpretava isso como "confirmado não-admin", redirecionando pra `/` **antes** do `useEffect` que busca o `role` sequer rodar. Corrigido inicializando `roleLoading` como `true` sempre que já existe sessão salva no primeiro render (`useState(() => initialSession() !== null)`), fechando a janela de corrida. Build, 16/16 testes e lint continuam limpos, `/admin` re-testado em produção.
