"""enable RLS and revoke anon/authenticated grants on alembic_version

Achado da auditoria das "5 falhas de vibe coding": a migration 0002
travou as 5 tabelas de negócio, mas a própria alembic_version (criada
automaticamente pelo Alembic, guarda qual migration está aplicada)
ficou de fora — anon/authenticated tinham DELETE/UPDATE/TRUNCATE nela,
o que permitiria corromper o controle de versão do schema de fora do
backend.

Revid: 0003
Revises: 0002
Create Date: 2026-08-13
"""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE alembic_version ENABLE ROW LEVEL SECURITY")
    op.execute("REVOKE ALL ON TABLE alembic_version FROM anon")
    op.execute("REVOKE ALL ON TABLE alembic_version FROM authenticated")


def downgrade() -> None:
    op.execute("ALTER TABLE alembic_version DISABLE ROW LEVEL SECURITY")
    op.execute(
        "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER "
        "ON TABLE alembic_version TO anon, authenticated"
    )
