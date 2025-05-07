import requests
from utils.config import SUBSCRIBER_PHONE

API_URL = "http://example.com/api"

def test_change_tariff_success(auth_header):
    response = requests.patch(f"{API_URL}/changeTariff/{SUBSCRIBER_PHONE}", headers=auth_header, json={
        "tariff_id": "11"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Tariff changed"

def test_change_tariff_invalid_id(auth_header):
    response = requests.patch(f"{API_URL}/changeTariff/{SUBSCRIBER_PHONE}", headers=auth_header, json={
        "tariff_id": "145351"
    })
    assert response.status_code == 400
    assert "error" in response.json()

def test_change_tariff_unauthorized():
    response = requests.patch(f"{API_URL}/changeTariff/{SUBSCRIBER_PHONE}", json={
        "tariff_id": "11"
    })
    assert response.status_code == 401
    assert "error" in response.json()
