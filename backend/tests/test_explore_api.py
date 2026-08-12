from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _payload(budget: float = 800, origin_city: str = "Belém", month: str = "Outubro"):
    return {"budget": budget, "origin_city": origin_city, "month": month}


def test_explore_returns_destinations_with_offers():
    response = client.post("/flights/explore", json=_payload(budget=800))

    assert response.status_code == 200
    body = response.json()
    assert body["search"]["origin_city"] == "Belém"
    assert len(body["destinations"]) > 0

    destination = body["destinations"][0]
    assert "best_offer" in destination
    assert "offers" in destination
    assert destination["best_offer"]["id"] in {o["id"] for o in destination["offers"]}


def test_explore_offer_ids_are_unique_across_destinations():
    response = client.post("/flights/explore", json=_payload(budget=5000))

    body = response.json()
    all_offer_ids = [
        offer["id"] for destination in body["destinations"] for offer in destination["offers"]
    ]
    assert len(all_offer_ids) == len(set(all_offer_ids))


def test_explore_rejects_non_positive_budget():
    response = client.post("/flights/explore", json=_payload(budget=0))

    assert response.status_code == 422


def test_explore_returns_near_budget_when_nothing_fits():
    response = client.post("/flights/explore", json=_payload(budget=1))

    body = response.json()
    assert body["destinations"] == []
    assert len(body["near_budget"]) >= 0
