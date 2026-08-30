"""Configuracion del backend (FASE 7)."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHASKIPE_", env_file=".env")

    app_name: str = "Chaski Pe API"
    version: str = "0.7.0"  # FASE 7
    environment: str = "development"

    # Origenes permitidos para CORS (el dev server de Vite).
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",  # vite preview
    ]

    # FASE 7: persistencia en memoria. La base de datos real es la FASE 8.
    persistence: str = "memory"


settings = Settings()
