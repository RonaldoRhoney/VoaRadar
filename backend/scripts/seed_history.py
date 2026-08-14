"""Popula o histórico de preços com o MockFlightProvider — uso local/dev.

    python -m scripts.seed_history [origem] [mes]

MOCK DATA: não representa preços reais. Serve pra ter histórico o
suficiente pro Analytics Engine (v0.3) ter o que analisar.
"""

import sys

from app.collectors.flight_collector import FlightCollector
from app.core.database import get_session_factory
from app.providers.mock_provider import MockFlightProvider
from app.repositories.notification_repository import NotificationRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository
from app.services.radar_evaluation_service import RadarEvaluationService


def main() -> None:
    origin_city = sys.argv[1] if len(sys.argv) > 1 else "Belém"
    month = sys.argv[2] if len(sys.argv) > 2 else "Outubro"

    session = get_session_factory()()
    try:
        repository = PriceHistoryRepository(session)
        # Único caminho de coleta hoje (RADAR_ENGINE.md §3) — precisa
        # acionar a avaliação de Radar igual a qualquer coleta real faria.
        radar_evaluator = RadarEvaluationService(
            repository, RadarRepository(session), NotificationRepository(session)
        )
        collector = FlightCollector(MockFlightProvider(), repository, radar_evaluator)
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
