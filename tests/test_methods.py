import pytest


@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_otros_metodos_devuelven_error(client, headers, method):
    r = getattr(client, method)("/DevOps", headers=headers)
    assert r.status_code == 405
    assert r.text == "ERROR"
