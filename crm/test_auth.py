import requests
import pytest
from utils.config import MANAGER_USERNAME, MANAGER_PASSWORD, SUBSCRIBER_PHONE
from tests.utils.auth import get_manager_token, get_subscriber_token

API_URL = "http://example.com/api"

def get_manager_token():
    r = requests.post(f"{API_URL}/auth", json={
        "login": MANAGER_USERNAME,
        "password": MANAGER_PASSWORD
    })
    return r.json()["token"]

def get_subscriber_token():
    r = requests.post(f"{API_URL}/auth", json={
        "phone": SUBSCRIBER_PHONE
    })
    return r.json()["token"]