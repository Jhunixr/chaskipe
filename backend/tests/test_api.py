"""Pruebas de la API (FASE 7)."""
from __future__ import annotations

from fastapi.testclient import TestClient

API = "/api/v1"


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["persistence"] == "memory"


def test_get_profile(client: TestClient) -> None:
    r = client.get(f"{API}/profile")
    assert r.status_code == 200
    assert set(r.json().keys()) == {"name", "email"}


def test_update_profile(client: TestClient) -> None:
    r = client.put(
        f"{API}/profile", json={"name": "Maria", "email": "maria@example.pe"}
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Maria"
    # persiste dentro de la misma sesion de proceso
    assert client.get(f"{API}/profile").json()["name"] == "Maria"


def test_update_profile_invalid(client: TestClient) -> None:
    assert (
        client.put(
            f"{API}/profile", json={"name": "", "email": "no-es-email"}
        ).status_code
        == 422
    )


def test_history_seed_and_order(client: TestClient) -> None:
    r = client.get(f"{API}/history")
    assert r.status_code == 200
    entries = r.json()
    assert len(entries) == 3
    times = [e["created_at"] for e in entries]
    assert times == sorted(times, reverse=True)


def test_history_create_and_delete(client: TestClient) -> None:
    r = client.post(
        f"{API}/history",
        json={"direction": "sign-to-text", "text": "Necesito ayuda"},
    )
    assert r.status_code == 201
    entry = r.json()
    assert entry["is_demo"] is True
    assert entry["id"]

    assert len(client.get(f"{API}/history").json()) == 4

    assert client.delete(f"{API}/history/{entry['id']}").status_code == 204
    assert len(client.get(f"{API}/history").json()) == 3


def test_history_delete_missing(client: TestClient) -> None:
    assert client.delete(f"{API}/history/nope").status_code == 404


def test_history_limit(client: TestClient) -> None:
    r = client.get(f"{API}/history", params={"limit": 2})
    assert len(r.json()) == 2


def test_history_clear(client: TestClient) -> None:
    r = client.delete(f"{API}/history")
    assert r.status_code == 200
    assert r.json()["deleted"] == 3
    assert client.get(f"{API}/history").json() == []


def test_history_invalid_direction(client: TestClient) -> None:
    r = client.post(
        f"{API}/history", json={"direction": "otra", "text": "x"}
    )
    assert r.status_code == 422


def test_phrases(client: TestClient) -> None:
    r = client.get(f"{API}/phrases")
    assert r.status_code == 200
    groups = r.json()
    assert [g["category"] for g in groups] == [
        "saludos",
        "necesidades",
        "emergencias",
    ]
    all_phrases = [p for g in groups for p in g["phrases"]]
    assert all(p["is_demo"] for p in all_phrases)
    assert any(p["text"] == "Necesito ayuda" for p in all_phrases)


def test_cors_headers(client: TestClient) -> None:
    r = client.get(
        f"{API}/profile", headers={"Origin": "http://localhost:5173"}
    )
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"
