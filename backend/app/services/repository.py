"""
Repositorio de datos (FASE 8).

`Repository` es la interfaz que usan los endpoints. Hay dos implementaciones:
- `MemoryRepository`  — todo en memoria (FASE 7, y fallback si no hay BD)
- `SqlRepository`     — PostgreSQL via SQLAlchemy (FASE 8)

`get_repository()` (en `app.services.store`) devuelve la que corresponda.
"""
from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone
from typing import Protocol

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.base import Frase, HistorialTraduccion, Usuario, get_session
from app.schemas.history import HistoryEntry, HistoryEntryCreate
from app.schemas.phrases import QuickPhrase, QuickPhraseGroup
from app.schemas.profile import Profile

USER_ID = 1  # FASE 8: un unico usuario

CATEGORY_LABELS = {
    "saludos": "Saludos",
    "necesidades": "Necesidades",
    "emergencias": "Emergencias",
}
CATEGORY_ORDER = ["saludos", "necesidades", "emergencias"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _seed_profile() -> Profile:
    return Profile(name="Andersson", email="andersson@example.pe")


def _seed_phrases() -> list[QuickPhrase]:
    """Frases semilla. `is_demo=True`: senas LSP no validadas."""
    raw = [
        ("ph-hola", "Hola", "saludos"),
        ("ph-gracias", "Gracias", "saludos"),
        ("ph-por-favor", "Por favor", "saludos"),
        ("ph-ayuda", "Necesito ayuda", "necesidades"),
        ("ph-no-entiendo", "No entiendo", "necesidades"),
        ("ph-bano", "¿Donde esta el bano?", "necesidades"),
        ("ph-emergencias", "Llame a emergencias", "emergencias"),
    ]
    return [
        QuickPhrase(id=i, text=t, category=c)  # type: ignore[arg-type]
        for i, t, c in raw
    ]


def _seed_history() -> list[tuple[str, str]]:
    return [
        ("sign-to-text", "Necesito ayuda"),
        ("text-to-sign", "Estoy bien, gracias."),
        ("sign-to-text", "Hola"),
    ]


def _group_phrases(phrases: list[QuickPhrase]) -> list[QuickPhraseGroup]:
    groups: list[QuickPhraseGroup] = []
    for cat in CATEGORY_ORDER:
        items = [p for p in phrases if p.category == cat]
        if items:
            groups.append(
                QuickPhraseGroup(
                    category=cat,  # type: ignore[arg-type]
                    label=CATEGORY_LABELS[cat],
                    phrases=items,
                )
            )
    return groups


class Repository(Protocol):
    def get_profile(self) -> Profile: ...
    def update_profile(self, name: str, email: str) -> Profile: ...
    def list_history(self, limit: int | None = None) -> list[HistoryEntry]: ...
    def add_history(self, data: HistoryEntryCreate) -> HistoryEntry: ...
    def delete_history(self, entry_id: str) -> bool: ...
    def clear_history(self) -> int: ...
    def list_phrase_groups(self) -> list[QuickPhraseGroup]: ...


# --------------------------------------------------------------------------
# Implementacion en memoria
# --------------------------------------------------------------------------


class MemoryRepository:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._profile = _seed_profile()
        self._phrases = _seed_phrases()
        self._history: list[HistoryEntry] = []
        for direction, text in _seed_history():
            self._history.append(
                HistoryEntry(
                    id=uuid.uuid4().hex[:12],
                    created_at=_now(),
                    direction=direction,  # type: ignore[arg-type]
                    text=text,
                    is_demo=True,
                )
            )

    def get_profile(self) -> Profile:
        with self._lock:
            return self._profile.model_copy()

    def update_profile(self, name: str, email: str) -> Profile:
        with self._lock:
            self._profile = Profile(name=name, email=email)
            return self._profile.model_copy()

    def list_history(self, limit: int | None = None) -> list[HistoryEntry]:
        with self._lock:
            items = sorted(
                self._history, key=lambda e: e.created_at, reverse=True
            )
            return items[:limit] if limit else list(items)

    def add_history(self, data: HistoryEntryCreate) -> HistoryEntry:
        with self._lock:
            entry = HistoryEntry(
                id=uuid.uuid4().hex[:12],
                created_at=_now(),
                **data.model_dump(),
            )
            self._history.append(entry)
            return entry

    def delete_history(self, entry_id: str) -> bool:
        with self._lock:
            before = len(self._history)
            self._history = [e for e in self._history if e.id != entry_id]
            return len(self._history) < before

    def clear_history(self) -> int:
        with self._lock:
            n = len(self._history)
            self._history = []
            return n

    def list_phrase_groups(self) -> list[QuickPhraseGroup]:
        with self._lock:
            return _group_phrases([p.model_copy() for p in self._phrases])


# --------------------------------------------------------------------------
# Implementacion PostgreSQL
# --------------------------------------------------------------------------


class SqlRepository:
    """Repositorio contra PostgreSQL. Una sesion corta por operacion."""

    def _session(self) -> Session:
        return get_session()

    # ---- Perfil ----
    def get_profile(self) -> Profile:
        with self._session() as s:
            user = s.get(Usuario, USER_ID)
            if user is None:
                seed = _seed_profile()
                user = Usuario(id=USER_ID, nombre=seed.name, correo=seed.email)
                s.add(user)
                s.commit()
            return Profile(name=user.nombre, email=user.correo)

    def update_profile(self, name: str, email: str) -> Profile:
        with self._session() as s:
            user = s.get(Usuario, USER_ID)
            if user is None:
                user = Usuario(id=USER_ID, nombre=name, correo=email)
                s.add(user)
            else:
                user.nombre = name
                user.correo = email
            s.commit()
            return Profile(name=user.nombre, email=user.correo)

    # ---- Historial ----
    def list_history(self, limit: int | None = None) -> list[HistoryEntry]:
        with self._session() as s:
            stmt = select(HistorialTraduccion).order_by(
                HistorialTraduccion.creado_en.desc()
            )
            if limit:
                stmt = stmt.limit(limit)
            rows = s.scalars(stmt).all()
            return [
                HistoryEntry(
                    id=r.id,
                    direction=r.direccion,  # type: ignore[arg-type]
                    text=r.texto,
                    is_demo=r.es_demo,
                    created_at=r.creado_en,
                )
                for r in rows
            ]

    def add_history(self, data: HistoryEntryCreate) -> HistoryEntry:
        with self._session() as s:
            row = HistorialTraduccion(
                id=uuid.uuid4().hex[:12],
                direccion=data.direction,
                texto=data.text,
                es_demo=data.is_demo,
                creado_en=_now(),
            )
            s.add(row)
            s.commit()
            return HistoryEntry(
                id=row.id,
                direction=row.direccion,  # type: ignore[arg-type]
                text=row.texto,
                is_demo=row.es_demo,
                created_at=row.creado_en,
            )

    def delete_history(self, entry_id: str) -> bool:
        with self._session() as s:
            row = s.get(HistorialTraduccion, entry_id)
            if row is None:
                return False
            s.delete(row)
            s.commit()
            return True

    def clear_history(self) -> int:
        with self._session() as s:
            result = s.execute(delete(HistorialTraduccion))
            s.commit()
            return int(result.rowcount or 0)

    # ---- Frases ----
    def list_phrase_groups(self) -> list[QuickPhraseGroup]:
        with self._session() as s:
            rows = s.scalars(
                select(Frase).order_by(Frase.categoria, Frase.orden)
            ).all()
            phrases = [
                QuickPhrase(
                    id=r.id,
                    text=r.texto,
                    category=r.categoria,  # type: ignore[arg-type]
                    is_demo=r.es_demo,
                )
                for r in rows
            ]
            return _group_phrases(phrases)


def seed_database() -> None:
    """Inserta los datos semilla si las tablas estan vacias."""
    with get_session() as s:
        if s.get(Usuario, USER_ID) is None:
            seed = _seed_profile()
            s.add(Usuario(id=USER_ID, nombre=seed.name, correo=seed.email))

        if s.scalar(select(Frase).limit(1)) is None:
            for order, p in enumerate(_seed_phrases()):
                s.add(
                    Frase(
                        id=p.id,
                        texto=p.text,
                        categoria=p.category,
                        orden=order,
                        es_demo=p.is_demo,
                    )
                )

        if s.scalar(select(HistorialTraduccion).limit(1)) is None:
            for direction, text in _seed_history():
                s.add(
                    HistorialTraduccion(
                        id=uuid.uuid4().hex[:12],
                        direccion=direction,
                        texto=text,
                        es_demo=True,
                        creado_en=_now(),
                    )
                )
        s.commit()
