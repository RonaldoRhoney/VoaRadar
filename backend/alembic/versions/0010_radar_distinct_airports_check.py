"""radars: CHECK origin_airport_id != destination_airport_id

Achado C da revisão manual: nada impedia criar/editar um Radar com
origem igual ao destino (inofensivo — nunca casaria com histórico real
— mas nonsense de produto). `routes` já tem essa mesma constraint desde
a v0.3 (0001); `radars` deveria ter nascido com ela também. A API já
valida isso na camada de schema/endpoint (RadarCreate/radars.py); esta
migration adiciona a mesma garantia no banco, defesa em profundidade.

Revision ID: 0010
Revises: 0009
Create Date: 2026-08-14
"""

from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_radar_distinct_airports", "radars", "origin_airport_id != destination_airport_id"
    )


def downgrade() -> None:
    op.drop_constraint("ck_radar_distinct_airports", "radars", type_="check")
