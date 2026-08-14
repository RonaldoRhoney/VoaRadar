"""cascade delete radar_events/notifications when a radar is deleted

Achado real ao testar DELETE /radars/{id} manualmente contra o Supabase:
sem ON DELETE CASCADE nas FKs de radar_id/radar_event_id, apagar um Radar
que já disparou pelo menos uma vez (tem radar_events/notifications)
quebra com IntegrityError — viraria um 500 cru pro usuário (CLAUDE.md
§15). Um Radar "dono" seu log de eventos e notificações — apagar o
Radar deve levar os dois junto, não deixar órfão nem bloquear a exclusão.

Revision ID: 0009
Revises: 0008
Create Date: 2026-08-14
"""

from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("radar_events_radar_id_fkey", "radar_events", type_="foreignkey")
    op.create_foreign_key(
        "radar_events_radar_id_fkey", "radar_events", "radars", ["radar_id"], ["id"], ondelete="CASCADE"
    )

    op.drop_constraint("notifications_radar_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key(
        "notifications_radar_id_fkey", "notifications", "radars", ["radar_id"], ["id"], ondelete="CASCADE"
    )

    op.drop_constraint("notifications_radar_event_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key(
        "notifications_radar_event_id_fkey",
        "notifications",
        "radar_events",
        ["radar_event_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("notifications_radar_event_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key(
        "notifications_radar_event_id_fkey", "notifications", "radar_events", ["radar_event_id"], ["id"]
    )

    op.drop_constraint("notifications_radar_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key("notifications_radar_id_fkey", "notifications", "radars", ["radar_id"], ["id"])

    op.drop_constraint("radar_events_radar_id_fkey", "radar_events", type_="foreignkey")
    op.create_foreign_key("radar_events_radar_id_fkey", "radar_events", "radars", ["radar_id"], ["id"])
