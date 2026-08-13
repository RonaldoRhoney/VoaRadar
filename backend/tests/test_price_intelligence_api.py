from datetime import date

from app.repositories.price_history_repository import PriceHistoryRepository


def _seed_offer(db_session, offer_id: str, prices: list[float]):
    repo = PriceHistoryRepository(db_session)
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = repo.get_or_create_airline("AD", "Azul")
    route = repo.get_or_create_route(origin.id, destination.id)

    for i, price in enumerate(prices):
        repo.record_observation(
            route_id=route.id,
            airline_id=airline.id,
            departure_date=date(2026, 10, 14 + i),
            return_date=date(2026, 10, 18 + i),
            stops=1,
            duration_minutes=260,
            provider="mock",
            provider_offer_id=offer_id if i == 0 else f"{offer_id}-hist-{i}",
            price=price,
            currency="BRL",
        )
    db_session.commit()


def test_price_intelligence_returns_analysis_for_known_offer(client, db_session):
    _seed_offer(db_session, "offer-rec-001", [399, 620, 890])

    response = client.get("/flights/price-intelligence/offer-rec-001", params={"price": 399})

    assert response.status_code == 200
    body = response.json()
    assert body["has_sufficient_data"] is True
    assert body["score"] == 100
    assert body["classification"] == "EXCELLENT"


def test_price_intelligence_returns_404_for_unknown_offer(client, db_session):
    response = client.get("/flights/price-intelligence/offer-que-nao-existe", params={"price": 500})

    assert response.status_code == 404
    assert "detail" in response.json()


def test_price_intelligence_rejects_non_positive_price(client, db_session):
    _seed_offer(db_session, "offer-rec-002", [399, 620])

    response = client.get("/flights/price-intelligence/offer-rec-002", params={"price": 0})

    assert response.status_code == 422


def test_price_intelligence_requires_price_query_param(client, db_session):
    response = client.get("/flights/price-intelligence/offer-rec-001")

    assert response.status_code == 422


def test_price_intelligence_rejects_non_finite_price(client, db_session):
    _seed_offer(db_session, "offer-rec-003", [399, 620])

    for value in ["inf", "-inf", "nan"]:
        response = client.get("/flights/price-intelligence/offer-rec-003", params={"price": value})
        assert response.status_code == 422, f"price={value} deveria ser rejeitado"


def test_price_intelligence_rejects_unrealistically_high_price(client, db_session):
    _seed_offer(db_session, "offer-rec-004", [399, 620])

    response = client.get("/flights/price-intelligence/offer-rec-004", params={"price": 9_999_999})

    assert response.status_code == 422
