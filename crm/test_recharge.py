import requests
from utils.config import SUBSCRIBER_PHONE

API_URL = "http://example.com/api"

def test_recharge_balance_success(auth_header):
    response = requests.post(f"{API_URL}/pay/{SUBSCRIBER_PHONE}", headers=auth_header, json={
        "money": 50
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Balance updated"

def test_recharge_invalid_amount(auth_header):
    response = requests.post(f"{API_URL}/pay/{SUBSCRIBER_PHONE}", headers=auth_header, json={
        "money": -20
    })
    assert response.status_code == 400
    assert "error" in response.json()

def test_recharge_without_auth():
    response = requests.post(f"{API_URL}/pay/{SUBSCRIBER_PHONE}", json={
        "money": 50
    })
    assert response.status_code == 401
    assert "error" in response.json()
