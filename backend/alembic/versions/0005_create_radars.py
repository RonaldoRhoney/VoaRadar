"""create radars (v0.4 — RLS + policy na mesma migration, SECURITY.md §1)

Revision ID: 0005
Revises: 0004
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "radars",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("origin_airport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("airports.id"), nullable=False),
        sa.Column("destination_airport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("airports.id"), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="ACTIVE"),
        sa.Column("condition_type", sa.String(32), nullable=False),
        sa.Column("condition_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("condition_classification", sa.String(32), nullable=True),
        sa.Column("last_event_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("last_event_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.CheckConstraint("status IN ('ACTIVE', 'PAUSED')", name="ck_radar_status"),
        sa.CheckConstraint(
            "condition_type IN ('PRICE_BELOW', 'OPPORTUNITY_CLASSIFICATION')", name="ck_radar_condition_type"
        ),
    )
    op.create_index("ix_radars_user_id", "radars", ["user_id"])
    op.create_index(
        "ix_radars_route_status", "radars", ["origin_airport_id", "destination_airport_id", "status"]
    )

    op.execute("ALTER TABLE radars ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY "own radars" ON radars
          FOR ALL USING (auth.uid() = user_id)
        """
    )
    # anon nunca acessa; authenticated só enxerga o que a policy libera —
    # mas o app fala com o backend, não direto com o Postgres, pra dado de
    # negócio (ARCHITECTURE.md §7). Grants aqui são defesa em profundidade,
    # não o caminho principal de acesso.
    op.execute("REVOKE ALL ON TABLE radars FROM anon")
    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE radars TO authenticated")


def downgrade() -> None:
    op.drop_table("radars")
