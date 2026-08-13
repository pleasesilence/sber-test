import pytest
from fastapi.testclient import TestClient

from main import app, store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    with store._lock:
        store._data.clear()


def test_root_endpoint_default_ip():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"client_ip": "testclient"}


def test_root_endpoint_x_forwarded_for_header():
    headers = {"x-forwarded-for": "203.0.113.195, 70.41.3.18, 150.172.238.178"}
    response = client.get("/", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"client_ip": "203.0.113.195"}


def test_root_endpoint_saves_name_when_provided():
    headers = {"x-forwarded-for": "198.51.100.1"}
    response = client.get("/?name=my-app", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"client_ip": "198.51.100.1"}

    assert store.get("my-app") == "198.51.100.1"


def test_resolve_existing_name():
    client.get("/?name=database", headers={"x-forwarded-for": "10.0.0.50"})

    response = client.get("/resolve/database")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "name": "database",
        "resolved_ip": "10.0.0.50",
    }


def test_resolve_nonexistent_name():
    response = client.get("/resolve/unknown-service")
    assert response.status_code == 200
    assert response.json() == {
        "status": "failure",
        "name": "unknown-service",
    }