"""radars: departure_date/return_date opcionais (ida e volta)

Pedido do usuário (2026-08-17): campo de ida e volta na criação de Radar
— até aqui o Radar vigiava a rota inteira, qualquer época. Colunas
nullable, Radar sem data continua funcionando exatamente como antes
(comportamento anterior preservado, não é breaking change).

Revision ID: 0014
Revises: 0013
Create Date: 2026-08-17
"""

import sqlalchemy as sa
from alembic import op

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("radars", sa.Column("departure_date", sa.Date(), nullable=True))
    op.add_column("radars", sa.Column("return_date", sa.Date(), nullable=True))
    op.create_check_constraint(
        "ck_radar_return_not_before_departure",
        "radars",
        "return_date IS NULL OR departure_date IS NULL OR return_date >= departure_date",
    )


def downgrade() -> None:
    op.drop_constraint("ck_radar_return_not_before_departure", "radars", type_="check")
    op.drop_column("radars", "return_date")
    op.drop_column("radars", "departure_date")
