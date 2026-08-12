from app.providers.base import FlightProvider
from app.providers.mock_provider import MockFlightProvider
from app.schemas.flight import (
    Destination,
    ExploreRequest,
    ExploreResponse,
    Metadata,
    RawDestination,
    SearchSummary,
)

# Quão acima do orçamento uma oferta ainda pode aparecer em "near_budget".
NEAR_BUDGET_MARGIN = 100


class ExploreService:
    def __init__(self, provider: FlightProvider | None = None):
        self._provider = provider or MockFlightProvider()

    def explore(self, request: ExploreRequest) -> ExploreResponse:
        raw_destinations = self._provider.get_destinations(
            origin_city=request.origin_city, month=request.month
        )

        within_budget = self._classify(raw_destinations, request.budget, "within_budget")
        near_budget = self._classify(
            raw_destinations,
            request.budget + NEAR_BUDGET_MARGIN,
            "near_budget",
            exclude_ids={d.id for d in within_budget},
        )

        within_budget = self._sort_by_price(within_budget)
        near_budget = self._sort_by_price(near_budget)
        self._apply_best_price_highlight(within_budget)

        prices = [d.best_offer.price for d in within_budget]

        return ExploreResponse(
            search=SearchSummary(
                origin_city=request.origin_city,
                budget=request.budget,
                month=request.month,
                flexible=request.flexible,
                passengers=request.passengers,
            ),
            destinations=within_budget,
            near_budget=near_budget,
            metadata=Metadata(
                result_count=len(within_budget),
                cheapest_price=min(prices) if prices else None,
            ),
        )

    def _classify(
        self,
        raw_destinations: list[RawDestination],
        price_ceiling: float,
        status: str,
        exclude_ids: set[str] | None = None,
    ) -> list[Destination]:
        exclude_ids = exclude_ids or set()
        result = []
        for raw in raw_destinations:
            if raw.id in exclude_ids:
                continue
            offers_within = [o for o in raw.offers if o.price <= price_ceiling]
            if not offers_within:
                continue
            best_offer = min(offers_within, key=lambda o: o.price)
            result.append(
                Destination(
                    id=raw.id,
                    city=raw.city,
                    uf=raw.uf,
                    budget_status=status,
                    highlight=None,
                    best_offer=best_offer,
                    offers=offers_within,
                )
            )
        return result

    def _sort_by_price(self, destinations: list[Destination]) -> list[Destination]:
        return sorted(destinations, key=lambda d: d.best_offer.price)

    def _apply_best_price_highlight(self, destinations: list[Destination]) -> None:
        if destinations:
            destinations[0].highlight = "best_price"
