"""Endpoints de las preferencias de accesibilidad."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas.preferences import Preferences, PreferencesUpdate
from app.services.store import get_repository

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=Preferences)
def get_preferences() -> Preferences:
    return get_repository().get_preferences()


@router.put("", response_model=Preferences)
def update_preferences(data: PreferencesUpdate) -> Preferences:
    return get_repository().update_preferences(Preferences(**data.model_dump()))
