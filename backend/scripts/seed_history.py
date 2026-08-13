"""Popula o histórico de preços com o MockFlightProvider — uso local/dev.

    python -m scripts.seed_history [origem] [mes]

MOCK DATA: não representa preços reais. Serve pra ter histórico o
suficiente pro Analytics Engine (v0.3) ter o que analisar.
"""

import sys

from app.collectors.flight_collector import FlightCollector
from app.core.database import get_session_factory
from app.providers.mock_provider import MockFlightProvider
from app.repositories.price_history_repository import PriceHistoryRepository


def main() -> None:
    origin_city = sys.argv[1] if len(sys.argv) > 1 else "Belém"
    month = sys.argv[2] if len(sys.argv) > 2 else "Outubro"

    session = get_session_factory()()
    try:
        repository = PriceHistoryRepository(session)
        collector = FlightCollector(MockFlightProvider(), repository)
        recorded = collector.collect(origin_city, month)
        session.commit()
        print(f"{recorded} observações de preço gravadas para {origin_city} ({month}).")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
