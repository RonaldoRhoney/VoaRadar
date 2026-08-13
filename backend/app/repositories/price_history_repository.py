import uuid
from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models import Airline, Airport, FlightObservation, PriceSnapshot, Route


class PriceHistoryRepository:
    """Único lugar que fala SQL/ORM nesta feature (ARCHITECTURE.md §4).

    `get_or_create_*` deixam a base de referência (aeroportos, companhias,
    rotas) idempotente — chamar de novo com os mesmos dados nunca duplica.
    `record_observation` é quem aplica a deduplicação de `FlightObservation`
    pela chave natural (ver docstring do model): a mesma combinação de
    rota/companhia/datas/escalas/duração/provider nunca vira uma linha nova,
    só um `PriceSnapshot` novo — é assim que o histórico de preço se forma.
    """

    def __init__(self, session: Session):
        self._session = session

    def get_or_create_airport(self, code: str, name: str, city: str, country: str) -> Airport:
        airport = self._session.query(Airport).filter_by(code=code).one_or_none()
        if airport is not None:
            return airport
        airport = Airport(code=code, name=name, city=city, country=country)
        self._session.add(airport)
        self._session.flush()
        return airport

    def get_or_create_airline(self, code: str, name: str) -> Airline:
        airline = self._session.query(Airline).filter_by(code=code).one_or_none()
        if airline is not None:
            return airline
        airline = Airline(code=code, name=name)
        self._session.add(airline)
        self._session.flush()
        return airline

    def get_or_create_route(self, origin_airport_id: uuid.UUID, destination_airport_id: uuid.UUID) -> Route:
        route = (
            self._session.query(Route)
            .filter_by(origin_airport_id=origin_airport_id, destination_airport_id=destination_airport_id)
            .one_or_none()
        )
        if route is not None:
            return route
        route = Route(origin_airport_id=origin_airport_id, destination_airport_id=destination_airport_id)
        self._session.add(route)
        self._session.flush()
        return route

    def record_observation(
        self,
        *,
        route_id: uuid.UUID,
        airline_id: uuid.UUID,
        departure_date: date,
        return_date: date | None,
        stops: int,
        duration_minutes: int,
        provider: str,
        provider_offer_id: str | None,
        price: float,
        currency: str,
        observed_at: datetime | None = None,
    ) -> PriceSnapshot:
        observation = (
            self._session.query(FlightObservation)
            .filter_by(
                route_id=route_id,
                airline_id=airline_id,
                departure_date=departure_date,
                return_date=return_date,
                stops=stops,
                duration_minutes=duration_minutes,
                provider=provider,
            )
            .one_or_none()
        )
        if observation is None:
            observation = FlightObservation(
                route_id=route_id,
                airline_id=airline_id,
                departure_date=departure_date,
                return_date=return_date,
                stops=stops,
                duration_minutes=duration_minutes,
                provider=provider,
                provider_offer_id=provider_offer_id,
            )
            self._session.add(observation)
            self._session.flush()

        snapshot_kwargs = {"flight_observation_id": observation.id, "price": price, "currency": currency}
        if observed_at is not None:
            snapshot_kwargs["observed_at"] = observed_at
        snapshot = PriceSnapshot(**snapshot_kwargs)
        self._session.add(snapshot)
        self._session.flush()
        return snapshot

    def get_price_history(self, route_id: uuid.UUID) -> list[float]:
        rows = (
            self._session.query(PriceSnapshot.price)
            .join(FlightObservation, PriceSnapshot.flight_observation_id == FlightObservation.id)
            .filter(FlightObservation.route_id == route_id)
            .all()
        )
        return [float(price) for (price,) in rows]

    def find_route_id_by_provider_offer_id(self, provider_offer_id: str) -> uuid.UUID | None:
        observation = (
            self._session.query(FlightObservation)
            .filter_by(provider_offer_id=provider_offer_id)
            .order_by(FlightObservation.created_at.desc())
            .first()
        )
        return observation.route_id if observation else None
