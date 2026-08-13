# Voa Radar — Auditoria de Segurança: RLS, permissões e regras de negócio

Data: 2026-08-13. Escopo: Row Level Security e grants no Supabase, separação de regra de negócio entre backend e frontend. Verificação feita com introspecção real no banco (`pg_class`, `pg_policies`, `information_schema.role_table_grants`), não por leitura de código.

## Achado crítico — RLS desabilitado + grants públicos de escrita/exclusão

Antes desta auditoria, nenhuma das 5 tabelas (`airports`, `airlines`, `routes`, `flight_observations`, `price_snapshots`) tinha Row Level Security habilitado, e os papéis `anon` e `authenticated` — usados pela API REST que o Supabase gera automaticamente pra todo projeto — tinham `SELECT`, `INSERT`, `UPDATE`, `DELETE` e `TRUNCATE` liberados em todas elas.

**Impacto real**: qualquer pessoa de posse da chave `anon` do projeto (uma chave pública por design — é normal ela ficar embutida em código de frontend) conseguia ler, alterar ou **apagar o histórico de preços inteiro** direto pela API REST do Supabase, sem passar pelo backend, sem autenticação nenhuma. Isso não é uma vulnerabilidade teórica — é o comportamento padrão do Supabase para tabelas criadas via SQL/migration direta (fora do fluxo do dashboard), que já vêm com esses grants aplicados automaticamente.

**Por que passou despercebido até agora**: as migrations anteriores (v0.3 FASE 1/2) focaram em criar o schema e validar que o *backend* conseguia ler/escrever — nunca se verificou o que um cliente *fora* do backend conseguia fazer.

## Correção aplicada

Migration `0002_enable_rls_and_lock_down_grants.py`:

```sql
ALTER TABLE <tabela> ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE <tabela> FROM anon;
REVOKE ALL ON TABLE <tabela> FROM authenticated;
```

Aplicada nas 5 tabelas. Nenhuma policy foi criada de propósito — a intenção é bloquear totalmente `anon`/`authenticated`, não abrir acesso condicional pra eles (não existe hoje nenhum caso de uso de acesso direto ao banco fora do backend).

**Por que isso não quebra o backend**: verificado via `pg_roles` que o papel de conexão do backend (`postgres`) tem `rolbypassrls = true` — dono de tabela bypassa RLS por padrão no Postgres, então a aplicação continua lendo/escrevendo normalmente. Confirmado ao vivo: 44/44 testes passando e uma consulta real (`analyze_offer`) funcionando sem alteração nenhuma no código da aplicação, só a migration.

**Defesa em profundidade**: RLS sozinho (sem policy) já bloquearia `anon`/`authenticated` completamente. O `REVOKE` é uma segunda camada independente — mesmo que uma policy permissiva fosse criada por engano no futuro, os grants revogados ainda impediriam o acesso.

## Verificação

| Checagem | Antes | Depois |
|---|---|---|
| RLS habilitado (5 tabelas) | ❌ não | ✅ sim |
| Grants de `anon`/`authenticated` | ✅ SELECT/INSERT/UPDATE/DELETE/TRUNCATE em todas | ✅ nenhum |
| Backend consegue ler/escrever | ✅ sim | ✅ sim (inalterado — `rolbypassrls`) |
| Rollback testado | — | ✅ `downgrade -1` → `upgrade head`, limpo |
| Testes | — | ✅ 44/44 |

## Auditoria de regras de negócio — backend vs. frontend

Verificado por busca no código-fonte (não por inferência): nenhum cálculo de preço, score, classificação de oportunidade ou status de orçamento existe no frontend. Tudo isso é produzido pelo backend (`app/analytics/engine.py`, `app/services/`) e o frontend só exibe o que recebe.

O único ponto que manipula dados de exploração no frontend é `features/explore/exploreFilters.ts` (`applyFilters`/`sortDestinations`): filtra e reordena a lista de destinos **já trazida do backend**, usando campos que o backend já calculou (`bestOffer.price`, `stops`, `durationMinutes`) — não recalcula `budget_status`, `highlight` nem nenhum score. Isso é refinamento de apresentação (equivalente a ordenar uma tabela na tela), não uma regra de negócio duplicada. Documentado aqui pra deixar claro que foi avaliado, não ignorado.

## Riscos residuais (aceitos por escopo, não corrigidos agora)

- **API do backend (`GET /flights/...`) continua sem autenticação** — por decisão de escopo já registrada (login fica pra v1.0, ver `docs/v0.3/PRD.md` §4 e a memória do projeto sobre padrão RhoneyInc de login). Isso é diferente do achado corrigido acima: aqui é a nossa própria API que decidimos deixar aberta; o problema corrigido era acesso *fora* da nossa API, direto no banco.
- **Sem rate limiting** — já registrado como pendência desde a auditoria da v0.2/v0.1, continua válido.
- **CORS** — segue restrito a `localhost:5173`, precisa de ajuste no deploy (já registrado no `ROADMAP.md`).

## Conclusão

O achado era de severidade crítica (leitura e destruição de dado sem autenticação, via canal fora do controle da aplicação) e afetava dado já em produção no Supabase real. Corrigido, verificado com introspecção real (antes/depois) e sem nenhum efeito colateral no funcionamento do backend. Regras de negócio confirmadas centralizadas no backend, sem duplicação no frontend.

---

## Revisão formal — as 5 falhas de vibe coding (2026-08-13)

Checklist baseado no vídeo "USOU VIBECODING? TÁ CORRENDO RISCO" (Mano Deyvin), trazido pelo usuário. Metodologia registrada em [../../../.claude/skills/vibe-coding-5-falhas/SKILL.md](../../../../.claude/skills/vibe-coding-5-falhas/SKILL.md) — checklist reutilizável pra qualquer produto RhoneyInc daqui pra frente.

### 1. RLS desativado — 🔴 CRÍTICO, corrigido

| Onde | O que |
|---|---|
| Banco Supabase (introspecção real, não arquivo) | 6 tabelas (`airports`, `airlines`, `routes`, `flight_observations`, `price_snapshots`, `alembic_version`) sem RLS, com `anon`/`authenticated` tendo SELECT/INSERT/UPDATE/DELETE/TRUNCATE liberados |
| `backend/alembic/versions/0002_enable_rls_and_lock_down_grants.py:29-35` | Correção das 5 tabelas de negócio |
| `backend/alembic/versions/0003_lock_down_alembic_version_table.py:22-24` | Correção da `alembic_version` — achada nesta revisão formal, tinha ficado de fora da 0002 por ser tabela de infraestrutura do Alembic, não "de negócio" |

Verificado: `SELECT relrowsecurity FROM pg_class` → `true` nas 6; `information_schema.role_table_grants` pra `anon`/`authenticated` → vazio nas 6.

### 2. Lógica de permissão no front-end — ✅ N/A

`grep -rniE "localStorage|sessionStorage|isAdmin|is_admin|role\s*===|permission" frontend/src` — zero ocorrências. Não existe login nem painel admin no Voa Radar ainda (fora do escopo até v1.0, ver `docs/v0.3/PRD.md` §4) — não há nada pra essa falha existir *em cima de*. Vale reavaliar no dia em que login for implementado.

### 3. IDOR — ✅ N/A por enquanto, anotado pra revisão futura

`backend/app/api/price_intelligence.py:15` é o único endpoint que recebe um ID de recurso (`offer_id`, na URL). Não há checagem de "dono" porque não existe conceito de dono — os dados de histórico de preço são agregados públicos por rota, não pertencem a um usuário. IDOR clássico pressupõe recurso privado de um usuário; isso não existe no Voa Radar ainda. **Registrado como ponto de atenção**: no dia em que login/dado pessoal entrar (buscas salvas, alertas — v0.4+), todo endpoint que já existir nessa época precisa ser revisado por este ângulo, não só os novos.

### 4. Chaves de API expostas — ✅ Limpo

- `grep -rniE "(api[_-]?key|secret[_-]?key|password|token)\s*[:=]\s*[\"'][a-zA-Z0-9]"` em todo o repo (`.py`, `.ts`, `.tsx`, `.js`, `.json`) — zero ocorrências.
- `git log --all --full-history -- "*.env" "backend/.env"` — `.env` nunca foi commitado, em nenhum commit do histórico.
- `backend/.env.example:3` e `frontend/.env.example:1` — só placeholders (`[SUA-SENHA]`, URL local).
- `frontend/dist/` (build de produção) — sem `sk-`, `SERVICE_ROLE` ou `SECRET`.
- Único uso de variável de ambiente no client (`frontend/src/services/api.ts:3`, `VITE_API_BASE_URL`) é uma URL, não um segredo — apropriado pra ir no bundle.

### 5. Falta de tratamento de input (XSS) — ✅ Limpo

- `grep -rn "dangerouslySetInnerHTML\|innerHTML\|eval("` em todo `frontend/src` — zero ocorrências (React escapa por padrão, e nada nesse código foge do padrão).
- Teste real (não só ausência de padrão perigoso): payload `<script>alert(1)</script>` enviado como `origin_city` real via URL — apareceu como texto puro na tela, nenhum alerta disparou (validado com Playwright na auditoria da v0.2, reconfirmado aqui pelo mesmo raciocínio já que nada mudou nessa área).
- Backend é API JSON pura (`fastapi`, sem `jinja2` nas dependências) — sem superfície de XSS server-side.

### Ferramenta de análise estática (sugerida no vídeo)

`bandit -r app/` e `bandit -r alembic/` — **0 issues** em 839 linhas (691 + 148). Executado nesta sessão.

### Resultado consolidado

| Falha | Status |
|---|---|
| 1. RLS desativado | 🔴→✅ Corrigido (2 tabelas achadas depois da correção inicial de v0.3 — a `alembic_version` foi um segundo achado nesta revisão) |
| 2. Permissão no front-end | ✅ N/A (sem login) |
| 3. IDOR | ✅ N/A (sem dado por usuário), anotado pra revisão quando login chegar |
| 4. Chaves expostas | ✅ Limpo |
| 5. XSS | ✅ Limpo |
