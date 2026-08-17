import uuid
from datetime import date

from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository
from app.services.radar_progress_service import RadarProgressService


def _seed_route_with_history(repo: PriceHistoryRepository, prices: list[float]):
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = repo.get_or_create_airline("AD", "Azul")
    route = repo.get_or_create_route(origin.id, destination.id)

    for i, price in enumerate(prices):
        repo.record_observation(
            route_id=route.id,
            airline_id=airline.id,
            departure_date=date(2026, 10, 14),
            return_date=date(2026, 10, 18),
            stops=1,
            duration_minutes=260,
            provider="mock",
            provider_offer_id=f"offer-rec-{i:03d}",
            price=price,
            currency="BRL",
        )
    return route


def _make_radar(radar_repo, route, **overrides):
    kwargs = {
        "user_id": uuid.uuid4(),
        "name": "Meu Radar Recife",
        "origin_airport_id": route.origin_airport_id,
        "destination_airport_id": route.destination_airport_id,
        "condition_type": "PRICE_BELOW",
        "condition_price": 500,
    }
    kwargs.update(overrides)
    return radar_repo.create(**kwargs)


def test_progress_e_none_quando_nao_ha_rota_com_historico(db_session):
    price_history_repo = PriceHistoryRepository(db_session)
    radar_repo = RadarRepository(db_session)
    origin = price_history_repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = price_history_repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    radar = radar_repo.create(
        user_id=uuid.uuid4(),
        name="Sem histórico ainda",
        origin_airport_id=origin.id,
        destination_airport_id=destination.id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    service = RadarProgressService(price_history_repo)

    assert service.compute(radar) is None


def test_price_below_progresso_e_alvo_sobre_menor_preco_visto(db_session):
    price_history_repo = PriceHistoryRepository(db_session)
    radar_repo = RadarRepository(db_session)
    route = _seed_route_with_history(price_history_repo, [800, 600, 750])
    radar = _make_radar(radar_repo, route, condition_price=480)
    db_session.commit()

    service = RadarProgressService(price_history_repo)

    # alvo 480 / menor preço já visto 600 = 80%
    assert service.compute(radar) == 80


def test_price_below_progresso_e_limitado_a_100(db_session):
    price_history_repo = PriceHistoryRepository(db_session)
    radar_repo = RadarRepository(db_session)
    route = _seed_route_with_history(price_history_repo, [400])
    radar = _make_radar(radar_repo, route, condition_price=500)
    db_session.commit()

    service = RadarProgressService(price_history_repo)

    assert service.compute(radar) == 100


def test_opportunity_classification_usa_score_do_preco_mais_recente(db_session):
    price_history_repo = PriceHistoryRepository(db_session)
    radar_repo = RadarRepository(db_session)
    route = _seed_route_with_history(price_history_repo, [1000, 800, 600])
    radar = _make_radar(
        radar_repo,
        route,
        condition_type="OPPORTUNITY_CLASSIFICATION",
        condition_price=None,
        condition_classification="EXCELLENT",
    )
    db_session.commit()

    service = RadarProgressService(price_history_repo)

    # preço mais recente (600) é o mínimo do histórico [1000, 800, 600] -> score 100
    assert service.compute(radar) == 100
