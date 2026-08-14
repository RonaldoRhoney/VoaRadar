# Voa Radar v0.4 — Segurança

Continuidade direta de `docs/v0.3/AUDIT_SECURITY.md` e da skill `.claude/skills/vibe-coding-5-falhas/SKILL.md`. Na v0.3, os itens 2 (permissão no front) e 3 (IDOR) eram N/A por não existir login. Na v0.4 deixam de ser N/A — é o primeiro teste real dessas duas falhas no projeto.

## 1. Regra de nascimento: toda tabela nova já vem com RLS + policy

Nenhuma migration de `radars`, `radar_events`, `notifications` ou `profiles` cria a tabela sem, na mesma migration, habilitar RLS e definir a policy — nunca "criar tabela" numa migration e "RLS" numa migration separada posterior (foi exatamente esse padrão que gerou o achado crítico da v0.3, DEC-021).

```sql
ALTER TABLE radars ENABLE ROW LEVEL SECURITY;
CREATE POLICY "own radars" ON radars
  FOR ALL USING (auth.uid() = user_id);
```

Mesma policy (adaptada) em `notifications` (via `user_id` denormalizado) e `radar_events` (via join com `radars.user_id`, ou `user_id` denormalizado também — decidir na implementação pelo custo de policy vs. denormalização).

## 2. RLS é camada extra, não a única barreira

Diferente do padrão "negar tudo" da v0.3 (onde `anon`/`authenticated` não tinham nenhum acesso e o backend, como dono das tabelas, fazia bypass de RLS), aqui o backend **continua** conectando como role que faz bypass de RLS — então a garantia real de isolamento entre usuários vive na query do repository (`WHERE id = :id AND user_id = :current_user_id`), com a policy de RLS como segunda camada independente, não como a única. Isso é decisão deliberada (ver `ARCHITECTURE.md` §7): o frontend não fala direto com o Postgres via PostgREST pra dado de negócio, só pra sessão do Supabase Auth.

## 3. Autenticação

JWT do Supabase Auth validado no backend (assinatura + expiração) a cada requisição autenticada, via dependency do FastAPI (`core/auth.py`). `user_id` só existe no backend como resultado dessa validação — nunca aceito de body/query/param do cliente. Nenhum endpoint de `radars`/`notifications` aceita `user_id` como parâmetro de entrada.

**Correção de achado real (DEC-111)**: a validação usa as chaves públicas do Supabase via JWKS (`/auth/v1/.well-known/jwks.json`, ES256), não um segredo HS256 compartilhado como planejado originalmente aqui — o painel do projeto (Settings > JWT Keys) mostrou que ele já usa o modelo novo de chaves assimétricas. Validado ao vivo: cadastro → login → token real → `GET /radars` autenticado.

## 4. IDOR — matriz de teste obrigatória

Antes do release da v0.4.0, testar explicitamente (automatizado, não manual):

| Cenário | Esperado |
|---|---|
| Usuário B tenta `GET /radars/{id_do_A}` | 404 |
| Usuário B tenta `PUT/PATCH /radars/{id_do_A}` | 404 |
| Usuário B tenta `DELETE /radars/{id_do_A}` | 404 |
| Usuário B tenta `PATCH /notifications/{id_do_A}/read` | 404 |
| Usuário não autenticado tenta qualquer endpoint de `/radars` ou `/notifications` | 401 |

**404, nunca 403**, em acesso cross-user — 403 confirmaria que o recurso existe, vazando informação sobre a existência de dado de outro usuário.

## 5. Chaves e segredos

Nenhuma mudança de princípio em relação à v0.3 (`AUDIT_SECURITY.md` item 4): chave do Supabase Auth usada no frontend é a `anon key` pública (apropriada para ir no bundle, por design do Supabase); qualquer chave de service role fica só no backend, em variável de ambiente, nunca commitada.

## 6. Auditoria formal FASE 9 (2026-08-14) — checklist completo das 5 falhas

Rodado contra o estado real: 92/92 pytest, Bandit limpo, backend com as migrations `0004`-`0010` aplicadas no Supabase real.

| Falha | Verificação | Resultado |
|---|---|---|
| 1. RLS desativado | `pg_class.relrowsecurity`, `information_schema.role_table_grants`, `pg_policies`, `pg_roles.rolbypassrls` — introspecção real no Postgres | ✅ 10 tabelas com RLS ativo (6 da v0.3 + `profiles`/`radars`/`radar_events`/`notifications`); `anon` sem nenhum grant; `authenticated` só com o escopo pretendido por tabela (`profiles`=SELECT, `radars`=SELECT/INSERT/UPDATE/DELETE, `radar_events`=SELECT, `notifications`=SELECT/UPDATE); backend (`postgres`) com `rolbypassrls=true`; 5 policies reais por `auth.uid()` |
| 2. Permissão no front-end | `grep -rniE "localStorage\|sessionStorage\|isAdmin\|is_admin\|role\s*===\|permission" frontend/src` | ✅ Único resultado é `features/auth/session.ts` guardando o token de sessão (opaco) em `localStorage` — não é decisão de permissão, é armazenamento de credencial; toda autorização é imposta no backend via validação de JWT (`core/auth.py`) + checagem de posse em cada repository |
| 3. IDOR | Todo endpoint com `{id}` (`GET/PUT/DELETE /radars/{id}`, `PATCH /notifications/{id}/read`) revisado; matriz automatizada rodada ao vivo | ✅ 10/10 testes de IDOR passando — usuário B sempre recebe 404 (nunca 403) ao tentar ler/editar/apagar recurso do usuário A; `RadarNotFoundError`/`NotificationNotFoundError` conflatam "não existe" e "não é seu" de propósito |
| 4. Chaves expostas | grep de segredo hardcoded no repo, `git log` do `.env`, grep no `dist/` de produção | ✅ Zero ocorrências de segredo hardcoded; `.env` nunca foi commitado (gitignorado desde a raiz); build de produção do frontend sem `sk-`/`SERVICE_ROLE`/`SECRET`; único uso de env var no client é `VITE_API_BASE_URL` (URL, não segredo) |
| 5. XSS | `grep -rn "dangerouslySetInnerHTML\|innerHTML\|eval(" frontend/src` | ✅ Zero ocorrências em todo o código novo da v0.4 (formulário de Radar, central de notificações, login/cadastro) — React escapa por padrão, mesma garantia já validada com payload real na v0.2 |

**Conclusão**: os 5 itens passam. Os itens 2 e 3, que eram N/A na v0.3 por não existir login, agora são testados de verdade — é o primeiro produto RhoneyInc a completar o checklist com dado real por usuário. Nenhum achado novo nesta rodada (os achados reais da v0.4 — grants automáticos, JWT via JWKS, cascade de exclusão, sino de notificações dessincronizado, validação de condição no PUT, origem=destino — já foram corrigidos e documentados em `DECISIONS.md` DEC-109 e DEC-111 a DEC-115 antes desta auditoria formal).

## 7. Achado real durante a FASE 5 — grants automáticos do Supabase vazando por baixo

Ao verificar as migrations `0004`-`0007` com introspecção real (mesma disciplina do `AUDIT_SECURITY.md` da v0.3), `authenticated` apareceu com `INSERT/UPDATE/DELETE/TRUNCATE/REFERENCES/TRIGGER` em todas as 4 tabelas novas — muito além do que cada migration concedia explicitamente (ex: `profiles` só deveria ter `SELECT`). Causa: o Supabase aplica `ALTER DEFAULT PRIVILEGES` automaticamente a toda tabela nova do schema `public`, concedendo acesso completo a `authenticated` antes de qualquer `GRANT` explícito da migration rodar — um `GRANT` seletivo é aditivo, não substitui esse padrão automático.

**Correção**: migration `0008` — `REVOKE ALL ON TABLE <t> FROM authenticated` antes de re-conceder exatamente o escopo pretendido em cada tabela. Verificado antes/depois via `information_schema.role_table_grants`; rollback testado (`downgrade -1` → `upgrade head`, limpo). Lição registrada em `DECISIONS.md` DEC-109: toda migration futura que crie tabela no `public` deve sempre `REVOKE ALL` antes de conceder qualquer coisa, nunca só `GRANT`.

## 7. Checklist de release da v0.4.0

Rodar a skill `vibe-coding-5-falhas` completa antes do release — desta vez com os 5 itens aplicáveis de verdade (2 e 3 deixam de ser N/A). Atualizar a tabela "Status por produto" da skill com o resultado.
