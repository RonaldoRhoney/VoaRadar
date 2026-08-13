"""enable RLS and revoke anon/authenticated grants on all tables

Achado de auditoria: nenhuma tabela tinha RLS habilitado, e os papéis
`anon`/`authenticated` (usados pela API REST auto-gerada do Supabase)
tinham SELECT/INSERT/UPDATE/DELETE/TRUNCATE liberados em todas elas —
qualquer pessoa com a chave anon do projeto (pública por design)
conseguia ler ou apagar o histórico de preço direto pela API do
Supabase, sem passar pelo backend.

O backend conecta como o papel `postgres`, que tem rolbypassrls=True
(confirmado via pg_roles) — habilitar RLS não afeta o funcionamento
do app em nada, só bloqueia o acesso via anon/authenticated.

Revid: 0002
Revises: 0001
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

TABLES = ["airports", "airlines", "routes", "flight_observations", "price_snapshots"]


def upgrade() -> None:
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        # Nenhuma policy é criada de propósito: o backend acessa como
        # dono da tabela (bypassa RLS por padrão no Postgres), e nenhum
        # outro papel deve ter acesso nenhum a estas tabelas por enquanto.
        op.execute(f"REVOKE ALL ON TABLE {table} FROM anon")
        op.execute(f"REVOKE ALL ON TABLE {table} FROM authenticated")


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
        # Restaura os grants automáticos que o Supabase aplica por padrão
        # em tabelas novas do schema public.
        op.execute(
            f"GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER "
            f"ON TABLE {table} TO anon, authenticated"
        )
