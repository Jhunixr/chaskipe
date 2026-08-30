"""Endpoints del historial de traducciones (FASE 7)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.history import HistoryEntry, HistoryEntryCreate
from app.services.store import store

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryEntry])
def list_history(
    limit: int | None = Query(default=None, ge=1, le=200),
) -> list[HistoryEntry]:
    return store.list_history(limit=limit)


@router.post("", response_model=HistoryEntry, status_code=status.HTTP_201_CREATED)
def add_history(data: HistoryEntryCreate) -> HistoryEntry:
    return store.add_history(data)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(entry_id: str) -> None:
    if not store.delete_history(entry_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de historial no encontrada",
        )


@router.delete("", status_code=status.HTTP_200_OK)
def clear_history() -> dict[str, int]:
    return {"deleted": store.clear_history()}
