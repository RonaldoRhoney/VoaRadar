import uuid
from datetime import date, datetime, timedelta, timezone

from app.repositories.notification_repository import NotificationRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository
from app.services.radar_evaluation_service import RadarEvaluationService


def _seed_route_with_history(repo: PriceHistoryRepository, prices: list[float]):
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = repo.get_or_create_airline("AD", "Azul")
    route = repo.get_or_create_route(origin.id, destination.id)

    last_snapshot = None
    for i, price in enumerate(prices):
        last_snapshot = repo.record_observation(
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
    return route, last_snapshot


def _make_service(db_session):
    price_history_repository = PriceHistoryRepository(db_session)
    radar_repository = RadarRepository(db_session)
    notification_repository = NotificationRepository(db_session)
    service = RadarEvaluationService(price_history_repository, radar_repository, notification_repository)
    return service, price_history_repository, radar_repository, notification_repository


def test_radar_price_below_dispara_e_notifica(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_id = uuid.uuid4()
    radar = radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()

    notifications = notification_repo.list_for_user(user_id)
    assert len(notifications) == 1
    assert notifications[0].radar_id == radar.id


def test_radar_nao_dispara_quando_condicao_nao_satisfeita(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_id = uuid.uuid4()
    radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=100,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()

    assert notification_repo.list_for_user(user_id) == []


def test_radar_pausado_nunca_e_avaliado(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_id = uuid.uuid4()
    radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        status="PAUSED",
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()

    assert notification_repo.list_for_user(user_id) == []


def test_cooldown_impede_segunda_notificacao_sem_queda_significativa(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_id = uuid.uuid4()
    radar = radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()
    assert len(notification_repo.list_for_user(user_id)) == 1

    # Segunda ocorrência, preço quase igual, dentro do cooldown — não deve notificar de novo.
    service.evaluate_for_route(route_id=route.id, current_price=428, price_snapshot_id=snapshot.id)
    db_session.commit()
    assert len(notification_repo.list_for_user(user_id)) == 1


def test_radar_event_e_gravado_mesmo_quando_cooldown_impede_notificacao(db_session):
    from app.models import RadarEvent

    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_id = uuid.uuid4()
    radar = radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    service.evaluate_for_route(route_id=route.id, current_price=428, price_snapshot_id=snapshot.id)
    db_session.commit()

    events = db_session.query(RadarEvent).filter_by(radar_id=radar.id).all()
    assert len(events) == 2
    assert len(notification_repo.list_for_user(user_id)) == 1


def test_multiplos_radares_na_mesma_rota_sao_avaliados_independentemente(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])

    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    radar_repo.create(
        user_id=user_a,
        name="Radar do A",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    radar_repo.create(
        user_id=user_b,
        name="Radar do B",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="PRICE_BELOW",
        condition_price=100,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()

    assert len(notification_repo.list_for_user(user_a)) == 1
    assert len(notification_repo.list_for_user(user_b)) == 0


def test_radar_de_outra_rota_nao_e_avaliado(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 640])
    other_origin = price_history_repo.get_or_create_airport("GRU", "Guarulhos", "São Paulo", "Brasil")
    other_destination = price_history_repo.get_or_create_airport("LIS", "Humberto Delgado", "Lisboa", "Portugal")

    user_id = uuid.uuid4()
    radar_repo.create(
        user_id=user_id,
        name="Radar de outra rota",
        origin_airport_id=other_origin.id,
        destination_airport_id=other_destination.id,
        condition_type="PRICE_BELOW",
        condition_price=99999,
    )
    db_session.commit()

    service.evaluate_for_route(route_id=route.id, current_price=429, price_snapshot_id=snapshot.id)
    db_session.commit()

    assert notification_repo.list_for_user(user_id) == []


def test_radar_por_classificacao_de_oportunidade(db_session):
    service, price_history_repo, radar_repo, notification_repo = _make_service(db_session)
    route, snapshot = _seed_route_with_history(price_history_repo, [600, 620, 900])

    user_id = uuid.uuid4()
    radar_repo.create(
        user_id=user_id,
        name="Radar por oportunidade",
        origin_airport_id=route.origin_airport_id,
        destination_airport_id=route.destination_airport_id,
        condition_type="OPPORTUNITY_CLASSIFICATION",
        condition_classification="EXCELLENT",
    )
    db_session.commit()

    # Preço no mínimo histórico → score 100 → EXCELLENT.
    service.evaluate_for_route(route_id=route.id, current_price=600, price_snapshot_id=snapshot.id)
    db_session.commit()

    assert len(notification_repo.list_for_user(user_id)) == 1
