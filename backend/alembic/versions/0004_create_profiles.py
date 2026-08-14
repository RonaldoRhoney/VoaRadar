"""create profiles (v0.4 — espelha auth.users, RLS nasce junto (SECURITY.md §1)

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id"], ["auth.users.id"], ondelete="CASCADE"),
    )

    op.execute("ALTER TABLE profiles ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY "own profile" ON profiles
          FOR ALL USING (auth.uid() = id)
        """
    )
    # anon nunca precisa ler/escrever profiles diretamente — só o backend
    # (que bypassa RLS) e o próprio dono via authenticated + policy acima.
    op.execute("REVOKE ALL ON TABLE profiles FROM anon")
    op.execute("GRANT SELECT ON TABLE profiles TO authenticated")


def downgrade() -> None:
    op.drop_table("profiles")
