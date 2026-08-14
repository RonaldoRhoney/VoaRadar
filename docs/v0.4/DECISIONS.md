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

## Pendência herdada da v0.3

Tag `v0.3.1` ainda não foi cortada para os 2 commits de segurança pós-`v0.3.0` (`b36e624`, `a7c698b`) — decisão já aprovada pelo usuário, execução ficou pausada quando o foco mudou para o planejamento da v0.4. Não bloqueia o início da v0.4, mas deve ser resolvida antes ou junto do início da FASE 5 do código, pra manter o histórico de tags coerente.
