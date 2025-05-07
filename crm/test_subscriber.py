import requests
from utils.config import SUBSCRIBER_PHONE

API_URL = "http://example.com/api"

def test_get_subscriber_info(auth_header):
    response = requests.get(f"{API_URL}/subscribers/{SUBSCRIBER_PHONE}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == SUBSCRIBER_PHONE
    assert "tariff" in data

def test_get_subscriber_info_unauthorized():
    response = requests.get(f"{API_URL}/subscribers/79991112233")
    assert response.status_code == 401
    assert "error" in response.json()

def test_get_subscriber_info_not_found(auth_header):
    response = requests.get(f"{API_URL}/subscribers/70000000000", headers=auth_header)
    assert response.status_code == 404
    assert "error" in response.json()

def test_create_subscriber_success(auth_header):
    payload = {"msisdn": "79992223344", "tariffId": 12}
    response = requests.post(f"{API_URL}/save", headers=auth_header, json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Subscriber created"

def test_create_subscriber_dublicate(auth_header):
    payload = {"msisdn": SUBSCRIBER_PHONE, "tariffId": 11}
    response = requests.post(f"{API_URL}/save", headers=auth_header, json=payload)
    assert response.status_code == 409
    assert "error" in response.json()