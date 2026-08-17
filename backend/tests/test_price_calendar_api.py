from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calendar_retorna_um_dia_por_dia_do_mes():
    response = client.get("/flights/calendar", params={"destination_id": "REC", "month": "2026-10"})

    assert response.status_code == 200
    body = response.json()
    assert body["destination_id"] == "REC"
    assert body["month"] == "2026-10"
    assert len(body["days"]) == 31  # outubro tem 31 dias
    assert body["days"][0]["date"] == "2026-10-01"
    assert body["days"][-1]["date"] == "2026-10-31"
    assert all(d["price"] > 0 for d in body["days"])


def test_calendar_respeita_numero_de_dias_do_mes():
    response = client.get("/flights/calendar", params={"destination_id": "REC", "month": "2026-02"})

    assert response.status_code == 200
    assert len(response.json()["days"]) == 28  # fevereiro de 2026 não é bissexto


def test_calendar_e_deterministico_mesma_entrada_mesmo_preco():
    first = client.get("/flights/calendar", params={"destination_id": "REC", "month": "2026-10"}).json()
    second = client.get("/flights/calendar", params={"destination_id": "REC", "month": "2026-10"}).json()

    assert first["days"] == second["days"]


def test_calendar_marca_o_dia_mais_barato_corretamente():
    response = client.get("/flights/calendar", params={"destination_id": "REC", "month": "2026-10"})

    body = response.json()
    cheapest_from_days = min(body["days"], key=lambda d: d["price"])
    assert body["cheapest_date"] == cheapest_from_days["date"]


def test_calendar_mes_com_formato_invalido_e_422():
    response = client.get("/flights/calendar", params={"destination_id": "REC", "month": "Outubro"})

    assert response.status_code == 422
    assert "AAAA-MM" in response.json()["detail"]


def test_calendar_destino_desconhecido_ainda_gera_precos_plausiveis():
    """Não deve quebrar — usa um preço-base padrão em vez de 500 erros pra
    um destino que não está no mock ainda."""
    response = client.get("/flights/calendar", params={"destination_id": "XYZ", "month": "2026-10"})

    assert response.status_code == 200
    assert len(response.json()["days"]) == 31
