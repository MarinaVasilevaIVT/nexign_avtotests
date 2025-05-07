import pytest
from utils.auth import get_manager_token, get_subscriber_token

@pytest.fixture(scope="session")
def manager_token():
    return get_manager_token()

@pytest.fixture(scope="session")
def subscriber_token():
    return get_subscriber_token()

@pytest.fixture
def auth_header(manager_token):
    return {"Authorization": f"Bearer {manager_token}"}