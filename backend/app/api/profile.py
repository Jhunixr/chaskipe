"""Endpoints del perfil (FASE 8)."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas.profile import Profile, ProfileUpdate
from app.services.store import get_repository

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=Profile)
def get_profile() -> Profile:
    return get_repository().get_profile()


@router.put("", response_model=Profile)
def update_profile(data: ProfileUpdate) -> Profile:
    return get_repository().update_profile(name=data.name, email=str(data.email))
