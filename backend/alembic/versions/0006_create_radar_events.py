"""create radar_events (v0.4 — log append-only, RLS via posse do radar)

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "radar_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("radar_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("radars.id"), nullable=False),
        sa.Column("price_snapshot_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("price_snapshots.id"), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("score", sa.Integer, nullable=True),
        sa.Column("classification", sa.String(32), nullable=True),
    )
    op.create_index("ix_radar_events_radar_id", "radar_events", ["radar_id"])

    op.execute("ALTER TABLE radar_events ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY "own radar events" ON radar_events
          FOR SELECT USING (
            EXISTS (SELECT 1 FROM radars WHERE radars.id = radar_events.radar_id AND radars.user_id = auth.uid())
          )
        """
    )
    # Nunca INSERT/UPDATE/DELETE pra authenticated — radar_events só é
    # escrito pelo backend (RadarEvaluationService), nunca pelo cliente.
    op.execute("REVOKE ALL ON TABLE radar_events FROM anon")
    op.execute("GRANT SELECT ON TABLE radar_events TO authenticated")


def downgrade() -> None:
    op.drop_table("radar_events")
