from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.store import store


@pytest.fixture
def client() -> TestClient:
    store.reset()
    return TestClient(app)
