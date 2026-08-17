from datetime import date

from app.repositories.price_history_repository import PriceHistoryRepository


def _make_route(repo: PriceHistoryRepository):
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = repo.get_or_create_airline("AZ", "Azul")
    route = repo.get_or_create_route(origin.id, destination.id)
    return route, airline


def _observation_kwargs(route, airline, **overrides):
    kwargs = {
        "route_id": route.id,
        "airline_id": airline.id,
        "departure_date": date(2026, 10, 14),
        "return_date": date(2026, 10, 18),
        "stops": 1,
        "duration_minutes": 260,
        "provider": "mock",
        "provider_offer_id": "offer-rec-001",
        "price": 429.0,
        "currency": "BRL",
    }
    kwargs.update(overrides)
    return kwargs


def test_get_or_create_airport_is_idempotent(db_session):
    repo = PriceHistoryRepository(db_session)

    first = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    second = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")

    assert first.id == second.id


def test_get_or_create_route_is_idempotent(db_session):
    repo = PriceHistoryRepository(db_session)
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")

    first = repo.get_or_create_route(origin.id, destination.id)
    second = repo.get_or_create_route(origin.id, destination.id)

    assert first.id == second.id


def test_record_observation_creates_flight_observation_and_snapshot(db_session):
    repo = PriceHistoryRepository(db_session)
    route, airline = _make_route(repo)

    repo.record_observation(**_observation_kwargs(route, airline))

    assert repo.get_price_history(route.id) == [429.0]


def test_repeated_observation_deduplicates_itinerary_but_adds_snapshot(db_session):
    from app.models import FlightObservation

    repo = PriceHistoryRepository(db_session)
    route, airline = _make_route(repo)

    repo.record_observation(**_observation_kwargs(route, airline, price=429.0))
    repo.record_observation(**_observation_kwargs(route, airline, price=462.0))

    assert sorted(repo.get_price_history(route.id)) == [429.0, 462.0]
    assert db_session.query(FlightObservation).filter_by(route_id=route.id).count() == 1


def test_different_itinerary_creates_a_new_flight_observation(db_session):
    from app.models import FlightObservation

    repo = PriceHistoryRepository(db_session)
    route, airline = _make_route(repo)

    repo.record_observation(**_observation_kwargs(route, airline, stops=1))
    repo.record_observation(**_observation_kwargs(route, airline, stops=0, duration_minutes=195))

    assert db_session.query(FlightObservation).filter_by(route_id=route.id).count() == 2
    assert sorted(repo.get_price_history(route.id)) == [429.0, 429.0]


def test_find_route_returns_none_when_no_route_exists(db_session):
    repo = PriceHistoryRepository(db_session)
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")

    assert repo.find_route(origin.id, destination.id) is None


def test_find_route_never_creates_a_route(db_session):
    from app.models import Route

    repo = PriceHistoryRepository(db_session)
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")

    repo.find_route(origin.id, destination.id)

    assert db_session.query(Route).count() == 0


def test_find_route_returns_existing_route(db_session):
    repo = PriceHistoryRepository(db_session)
    route, _ = _make_route(repo)

    found = repo.find_route(route.origin_airport_id, route.destination_airport_id)

    assert found is not None
    assert found.id == route.id


def test_get_price_history_is_scoped_to_route(db_session):
    repo = PriceHistoryRepository(db_session)
    route_a, airline = _make_route(repo)
    other_destination = repo.get_or_create_airport("FOR", "Pinto Martins", "Fortaleza", "Brasil")
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    route_b = repo.get_or_create_route(origin.id, other_destination.id)

    repo.record_observation(**_observation_kwargs(route_a, airline, price=429.0))
    repo.record_observation(**_observation_kwargs(route_b, airline, price=517.0))

    assert repo.get_price_history(route_a.id) == [429.0]
    assert repo.get_price_history(route_b.id) == [517.0]
