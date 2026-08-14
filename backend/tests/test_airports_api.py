from app.repositories.price_history_repository import PriceHistoryRepository


def test_lista_aeroportos_publica_sem_autenticacao(client, db_session):
    repo = PriceHistoryRepository(db_session)
    repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    db_session.commit()

    response = client.get("/airports")

    assert response.status_code == 200
    codes = {a["code"] for a in response.json()}
    assert codes == {"BEL", "REC"}


def test_lista_aeroportos_vazia_quando_nao_ha_dado(client, db_session):
    response = client.get("/airports")

    assert response.status_code == 200
    assert response.json() == []
