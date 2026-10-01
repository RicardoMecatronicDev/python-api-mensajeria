import os

import pytest
from fastapi.testclient import TestClient

os.environ["API_KEY"] = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
os.environ["JWT_SECRET"] = "secreto-solo-para-tests-0123456789abcdef"

from app.main import app, seen_jtis
from app.security import create_jwt

API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
PAYLOAD = {
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45,
}


@pytest.fixture(autouse=True)
def _clean_jtis():
    seen_jtis.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def headers():
    return {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": create_jwt(),
        "Content-Type": "application/json",
    }
