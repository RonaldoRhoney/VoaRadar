"""create notifications (v0.4 — user_id denormalizado, RLS direta)

Revision ID: 0007
Revises: 0006
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("radar_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("radars.id"), nullable=False),
        sa.Column("radar_event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("radar_events.id"), nullable=False),
        sa.Column("type", sa.String(32), nullable=False, server_default="OPPORTUNITY_FOUND"),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message", sa.String(500), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])

    op.execute("ALTER TABLE notifications ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY "own notifications" ON notifications
          FOR SELECT USING (auth.uid() = user_id)
        """
    )
    op.execute(
        """
        CREATE POLICY "mark own notifications read" ON notifications
          FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id)
        """
    )
    # INSERT continua só pelo backend (bypassa RLS) — notification nunca é
    # criada pelo cliente diretamente.
    op.execute("REVOKE ALL ON TABLE notifications FROM anon")
    op.execute("GRANT SELECT, UPDATE ON TABLE notifications TO authenticated")


def downgrade() -> None:
    op.drop_table("notifications")
