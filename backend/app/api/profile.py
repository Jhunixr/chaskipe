"""Endpoints del perfil (FASE 7)."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas.profile import Profile, ProfileUpdate
from app.services.store import store

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=Profile)
def get_profile() -> Profile:
    return store.get_profile()


@router.put("", response_model=Profile)
def update_profile(data: ProfileUpdate) -> Profile:
    return store.update_profile(name=data.name, email=str(data.email))
