from tests.conftest import PAYLOAD


def test_post_valido_devuelve_mensaje(client, headers):
    r = client.post("/DevOps", json=PAYLOAD, headers=headers)
    assert r.status_code == 200
    assert r.json() == {"message": "Hello Juan Perez your message will be sent"}


def test_body_invalido_devuelve_422(client, headers):
    r = client.post("/DevOps", json={"message": "x"}, headers=headers)
    assert r.status_code == 422


def test_ttl_debe_ser_positivo(client, headers):
    r = client.post("/DevOps", json={**PAYLOAD, "timeToLifeSec": 0}, headers=headers)
    assert r.status_code == 422


def test_health(client):
    assert client.get("/health").status_code == 200
