"""
Almacen en memoria (FASE 7).

Todo vive en variables de proceso: se pierde al reiniciar. La base de datos
real (PostgreSQL) es la FASE 8; esta capa se reemplazara por un repositorio
contra la BD manteniendo la misma interfaz.

FASE 7 asume un unico usuario (no hay autenticacion todavia).
"""
from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone

from app.schemas.history import HistoryEntry, HistoryEntryCreate
from app.schemas.phrases import QuickPhrase, QuickPhraseGroup
from app.schemas.profile import Profile

_lock = threading.Lock()


def _now() -> datetime:
    return datetime.now(timezone.utc)


class MemoryStore:
    """Estado del proceso. Una instancia global: `store`."""

    def __init__(self) -> None:
        self._profile = Profile(name="Andersson", email="andersson@example.pe")
        self._history: list[HistoryEntry] = []
        self._phrase_groups = _seed_phrases()
        self._seed_history()

    # ---- Perfil ----
    def get_profile(self) -> Profile:
        with _lock:
            return self._profile.model_copy()

    def update_profile(self, name: str, email: str) -> Profile:
        with _lock:
            self._profile = Profile(name=name, email=email)
            return self._profile.model_copy()

    # ---- Historial ----
    def list_history(self, limit: int | None = None) -> list[HistoryEntry]:
        with _lock:
            items = sorted(
                self._history, key=lambda e: e.created_at, reverse=True
            )
            return items[:limit] if limit else list(items)

    def add_history(self, data: HistoryEntryCreate) -> HistoryEntry:
        with _lock:
            entry = HistoryEntry(
                id=uuid.uuid4().hex[:12],
                created_at=_now(),
                **data.model_dump(),
            )
            self._history.append(entry)
            return entry

    def delete_history(self, entry_id: str) -> bool:
        with _lock:
            before = len(self._history)
            self._history = [e for e in self._history if e.id != entry_id]
            return len(self._history) < before

    def clear_history(self) -> int:
        with _lock:
            n = len(self._history)
            self._history = []
            return n

    # ---- Frases rapidas ----
    def list_phrase_groups(self) -> list[QuickPhraseGroup]:
        with _lock:
            return [g.model_copy(deep=True) for g in self._phrase_groups]

    # ---- Utilidad para tests ----
    def reset(self) -> None:
        with _lock:
            self.__init__()  # type: ignore[misc]

    def _seed_history(self) -> None:
        seed = [
            ("sign-to-text", "Necesito ayuda"),
            ("text-to-sign", "Estoy bien, gracias."),
            ("sign-to-text", "Hola"),
        ]
        for direction, text in seed:
            self._history.append(
                HistoryEntry(
                    id=uuid.uuid4().hex[:12],
                    created_at=_now(),
                    direction=direction,  # type: ignore[arg-type]
                    text=text,
                    is_demo=True,
                )
            )


def _seed_phrases() -> list[QuickPhraseGroup]:
    """
    Frases semilla. Las senas LSP asociadas NO estan validadas: `is_demo=True`.
    """
    return [
        QuickPhraseGroup(
            category="saludos",
            label="Saludos",
            phrases=[
                QuickPhrase(id="ph-hola", text="Hola", category="saludos"),
                QuickPhrase(id="ph-gracias", text="Gracias", category="saludos"),
                QuickPhrase(
                    id="ph-por-favor", text="Por favor", category="saludos"
                ),
            ],
        ),
        QuickPhraseGroup(
            category="necesidades",
            label="Necesidades",
            phrases=[
                QuickPhrase(
                    id="ph-ayuda", text="Necesito ayuda", category="necesidades"
                ),
                QuickPhrase(
                    id="ph-no-entiendo",
                    text="No entiendo",
                    category="necesidades",
                ),
                QuickPhrase(
                    id="ph-bano",
                    text="¿Donde esta el bano?",
                    category="necesidades",
                ),
            ],
        ),
        QuickPhraseGroup(
            category="emergencias",
            label="Emergencias",
            phrases=[
                QuickPhrase(
                    id="ph-emergencias",
                    text="Llame a emergencias",
                    category="emergencias",
                ),
            ],
        ),
    ]


store = MemoryStore()
