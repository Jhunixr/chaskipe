"""
Pruebas de la capa de persistencia (FASE 8).

- La seleccion de repositorio y el fallback a memoria se prueban siempre.
- La integracion con PostgreSQL solo si hay una base de datos disponible
  (se salta en caso contrario).
"""
from __future__ import annotations

import pytest

from app.core.config import settings
from app.db.base import init_engine
from app.schemas.history import HistoryEntryCreate
from app.services import store
from app.services.repository import MemoryRepository, SqlRepository

_DB_AVAILABLE = init_engine()


def test_fallback_to_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    """Si la BD no conecta, se usa MemoryRepository y no se lanza excepcion."""
    monkeypatch.setattr(store.db, "init_engine", lambda: False)
    monkeypatch.setattr(settings, "require_database", False)
    backend = store.configure_repository()
    assert backend == "memory"
    assert isinstance(store.get_repository(), MemoryRepository)


def test_require_database_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(store.db, "init_engine", lambda: False)
    monkeypatch.setattr(settings, "require_database", True)
    with pytest.raises(RuntimeError):
        store.configure_repository()


@pytest.mark.skipif(not _DB_AVAILABLE, reason="PostgreSQL no disponible")
def test_sql_repository_roundtrip() -> None:
    store.configure_repository()
    assert store.current_backend() == "postgresql"
    repo = SqlRepository()

    # perfil
    repo.update_profile("Test PG", "pg@test.pe")
    assert repo.get_profile().name == "Test PG"
    repo.update_profile("Andersson", "andersson@example.pe")  # restaurar

    # historial: crear, listar, borrar
    entry = repo.add_history(
        HistoryEntryCreate(direction="sign-to-text", text="Prueba integracion")
    )
    ids = [e.id for e in repo.list_history()]
    assert entry.id in ids
    assert repo.delete_history(entry.id) is True
    assert repo.delete_history(entry.id) is False

    # frases
    groups = repo.list_phrase_groups()
    assert [g.category for g in groups] == [
        "saludos",
        "necesidades",
        "emergencias",
    ]
