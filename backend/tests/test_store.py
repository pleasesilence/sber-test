import time
from unittest.mock import patch
import pytest

from main import TTLStore


def test_ttl_store_set_and_get():
    store = TTLStore()
    store.set("service-a", "192.168.1.10", ttl_seconds=60)
    assert store.get("service-a") == "192.168.1.10"


def test_ttl_store_get_nonexistent():
    store = TTLStore()
    assert store.get("nonexistent") is None


def test_ttl_store_expired_entry():
    store = TTLStore()

    with patch("time.monotonic") as mock_time:
        mock_time.return_value = 100.0
        store.set("service-b", "10.0.0.1", ttl_seconds=10)

        mock_time.return_value = 105.0
        assert store.get("service-b") == "10.0.0.1"

        mock_time.return_value = 111.0
        assert store.get("service-b") is None

        assert "service-b" not in store._data


def test_ttl_store_overwrite_existing():
    store = TTLStore()
    store.set("service-c", "1.1.1.1", ttl_seconds=60)
    store.set("service-c", "2.2.2.2", ttl_seconds=120)
    assert store.get("service-c") == "2.2.2.2"