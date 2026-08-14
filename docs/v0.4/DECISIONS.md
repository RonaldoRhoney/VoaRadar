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

## Melhoria futura identificada — skill `admin-padrao` (RhoneyInc)

A skill `admin-padrao` (`.claude/skills/admin-padrao/SKILL.md`) exige que todo produto RhoneyInc com conceito de admin promova `rhoneyinc@gmail.com` automaticamente. A v0.4 introduz `profiles` (primeira tabela de usuário do Voa Radar), mas **sem** coluna `role` nem painel administrativo — não há "admin" a promover ainda, então a skill não se aplica hoje. Registrado aqui para não ser esquecido: no dia em que um papel de admin for desenhado pro Voa Radar (fora do escopo da v0.4, nenhum pedido do usuário até agora), aplicar o trigger `handle_new_user()` do mesmo padrão do hub RhoneyInc.

## Pendência herdada da v0.3

Tag `v0.3.1` ainda não foi cortada para os 2 commits de segurança pós-`v0.3.0` (`b36e624`, `a7c698b`) — decisão já aprovada pelo usuário, execução ficou pausada quando o foco mudou para o planejamento da v0.4. Não bloqueia o início da v0.4, mas deve ser resolvida antes ou junto do início da FASE 5 do código, pra manter o histórico de tags coerente.
