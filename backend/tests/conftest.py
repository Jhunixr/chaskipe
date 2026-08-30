from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import app.services.store as store_module
from app.main import app
from app.services.store import use_memory_repository


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """
    Cliente de la API contra el repositorio EN MEMORIA: rapido y sin
    necesidad de PostgreSQL. Se neutraliza el lifespan que intentaria
    conectar a la base de datos.
    """

    def _memory_only() -> str:
        use_memory_repository()
        return "memory"

    monkeypatch.setattr(store_module, "configure_repository", _memory_only)
    use_memory_repository()
    with TestClient(app) as c:
        yield c
