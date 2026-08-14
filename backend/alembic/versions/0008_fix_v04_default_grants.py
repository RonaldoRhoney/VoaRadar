"""fix v0.4 tables: revoke Supabase's automatic default grants before re-granting

Achado ao verificar 0004-0007 com introspecção real (mesmo padrão da
auditoria da v0.3, DEC-021): o Supabase concede automaticamente
INSERT/UPDATE/DELETE/TRUNCATE/REFERENCES/TRIGGER a `authenticated` em
toda tabela nova do schema `public` (ALTER DEFAULT PRIVILEGES do
projeto). As migrations 0004-0007 só faziam GRANT adicional — nunca um
REVOKE ALL antes —, então o grant automático do Supabase continuou
valendo por baixo, dando a `authenticated` acesso completo (incluindo
DELETE/TRUNCATE em `profiles` e `radar_events`, que deveriam ser
somente leitura) em vez do escopo pretendido em cada migration.

Revision ID: 0008
Revises: 0007
Create Date: 2026-08-14
"""

from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None

# tabela -> privilégios que authenticated deveria ter, replicando a
# intenção original de cada migration (0004-0007)
INTENDED_GRANTS = {
    "profiles": "SELECT",
    "radars": "SELECT, INSERT, UPDATE, DELETE",
    "radar_events": "SELECT",
    "notifications": "SELECT, UPDATE",
}


def upgrade() -> None:
    for table, grants in INTENDED_GRANTS.items():
        op.execute(f"REVOKE ALL ON TABLE {table} FROM authenticated")
        op.execute(f"GRANT {grants} ON TABLE {table} TO authenticated")


def downgrade() -> None:
    for table in INTENDED_GRANTS:
        op.execute(
            f"GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER "
            f"ON TABLE {table} TO authenticated"
        )
