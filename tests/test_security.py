import time

import jwt

from app.security import JWT_ALGORITHM, JWT_SECRET, create_jwt
from tests.conftest import API_KEY, PAYLOAD


def test_sin_api_key_401(client, headers):
    headers.pop("X-Parse-REST-API-Key")
    r = client.post("/DevOps", json=PAYLOAD, headers=headers)
    assert r.status_code == 401
    assert r.text == "ERROR"


def test_api_key_incorrecta_401(client, headers):
    headers["X-Parse-REST-API-Key"] = "mala"
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_sin_jwt_401(client, headers):
    headers.pop("X-JWT-KWY")
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_jwt_firma_invalida_401(client, headers):
    headers["X-JWT-KWY"] = jwt.encode({"jti": "a", "exp": time.time() + 60}, "otra", JWT_ALGORITHM)
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_jwt_expirado_401(client, headers):
    token = jwt.encode({"jti": "a", "exp": time.time() - 10}, JWT_SECRET, JWT_ALGORITHM)
    headers["X-JWT-KWY"] = token
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_jwt_sin_jti_401(client, headers):
    token = jwt.encode({"exp": time.time() + 60}, JWT_SECRET, JWT_ALGORITHM)
    headers["X-JWT-KWY"] = token
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_jwt_reutilizado_401(client, headers):
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 200
    assert client.post("/DevOps", json=PAYLOAD, headers=headers).status_code == 401


def test_cada_jwt_es_unico():
    primero = create_jwt()
    segundo = create_jwt()
    assert primero != segundo


def test_api_key_constante_correcta():
    assert API_KEY == "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
