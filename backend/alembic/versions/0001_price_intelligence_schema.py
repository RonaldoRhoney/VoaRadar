"""price intelligence schema (airports, airlines, routes, flight_observations, price_snapshots)

Revision ID: 0001
Revises:
Create Date: 2026-08-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "airports",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("code", sa.String(3), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(255), nullable=False),
        sa.Column("country", sa.String(255), nullable=False),
        sa.UniqueConstraint("code", name="uq_airports_code"),
    )
    op.create_index("ix_airports_code", "airports", ["code"])

    op.create_table(
        "airlines",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("code", sa.String(8), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.UniqueConstraint("code", name="uq_airlines_code"),
    )
    op.create_index("ix_airlines_code", "airlines", ["code"])

    op.create_table(
        "routes",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("origin_airport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("airports.id"), nullable=False),
        sa.Column("destination_airport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("airports.id"), nullable=False),
        sa.CheckConstraint("origin_airport_id != destination_airport_id", name="ck_route_distinct_airports"),
        sa.UniqueConstraint("origin_airport_id", "destination_airport_id", name="uq_route_origin_destination"),
    )
    op.create_index("ix_routes_origin_airport_id", "routes", ["origin_airport_id"])
    op.create_index("ix_routes_destination_airport_id", "routes", ["destination_airport_id"])

    op.create_table(
        "flight_observations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("route_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("airline_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("airlines.id"), nullable=False),
        sa.Column("departure_date", sa.Date, nullable=False),
        sa.Column("return_date", sa.Date, nullable=True),
        sa.Column("stops", sa.Integer, nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("provider_offer_id", sa.String(255), nullable=True),
        sa.UniqueConstraint(
            "route_id", "airline_id", "departure_date", "return_date", "stops", "duration_minutes", "provider",
            name="uq_flight_observation_itinerary",
        ),
    )
    op.create_index("ix_flight_observations_route_id", "flight_observations", ["route_id"])
    op.create_index("ix_flight_observations_airline_id", "flight_observations", ["airline_id"])
    op.create_index("ix_flight_observations_departure_date", "flight_observations", ["departure_date"])

    op.create_table(
        "price_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("flight_observation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("flight_observations.id"), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_price_snapshots_flight_observation_id", "price_snapshots", ["flight_observation_id"])
    op.create_index("ix_price_snapshots_price", "price_snapshots", ["price"])
    op.create_index("ix_price_snapshots_observed_at", "price_snapshots", ["observed_at"])


def downgrade() -> None:
    op.drop_table("price_snapshots")
    op.drop_table("flight_observations")
    op.drop_table("routes")
    op.drop_table("airlines")
    op.drop_table("airports")
