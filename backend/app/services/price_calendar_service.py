from app.providers.base import FlightProvider
from app.providers.mock_provider import MockFlightProvider
from app.schemas.flight import PriceCalendarResponse


class PriceCalendarService:
    def __init__(self, provider: FlightProvider | None = None):
        self._provider = provider or MockFlightProvider()

    def get_calendar(self, destination_id: str, month: str) -> PriceCalendarResponse:
        days = self._provider.get_price_calendar(destination_id, month)
        cheapest = min(days, key=lambda d: d.price) if days else None
        return PriceCalendarResponse(
            destination_id=destination_id,
            month=month,
            days=days,
            cheapest_date=cheapest.date if cheapest else None,
        )
