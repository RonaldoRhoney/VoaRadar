"""create anac_fare_reference (Zero-Cost API First, DEC-117 — PA.2)

Tarifa média mensal por rota, importada offline dos dados abertos da
ANAC (docs/PROVIDER_ARCHITECTURE.md). Nunca uma oferta comprável — só
referência histórica. RLS habilitado, sem grant pra anon/authenticated
(mesmo padrão de airports/routes/price_snapshots, migration 0002) —
dado de referência público, mas escrito só pelo script de importação
offline (backend, dono da tabela).

Revision ID: 0012
Revises: 0011
Create Date: 2026-08-16
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "anac_fare_reference",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("route_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("reference_month", sa.String(7), nullable=False),
        sa.Column("average_fare", sa.Numeric(10, 2), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=True),
        sa.Column("source_url", sa.String(500), nullable=False),
        sa.Column("imported_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("route_id", "reference_month", name="uq_anac_fare_route_month"),
    )
    op.create_index("ix_anac_fare_reference_route_id", "anac_fare_reference", ["route_id"])

    op.execute("ALTER TABLE anac_fare_reference ENABLE ROW LEVEL SECURITY")
    op.execute("REVOKE ALL ON TABLE anac_fare_reference FROM anon")
    op.execute("REVOKE ALL ON TABLE anac_fare_reference FROM authenticated")


def downgrade() -> None:
    op.drop_table("anac_fare_reference")
