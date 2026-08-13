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
