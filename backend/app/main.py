"""
Punto de entrada de la API de Chaski Pe (FASE 7).

    cd backend
    .venv\\Scripts\\activate
    uvicorn app.main:app --reload

Docs interactivas: http://127.0.0.1:8000/docs

Alcance FASE 7:
- Perfil, historial y frases rapidas.
- Persistencia EN MEMORIA (se pierde al reiniciar). PostgreSQL es la FASE 8.
- Sin autenticacion. Sin endpoint de inferencia (el modelo corre en el navegador).
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import history, phrases, profile
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    summary="API de perfil, historial y frases rapidas de Chaski Pe.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "persistence": settings.persistence,
    }


API_PREFIX = "/api/v1"
app.include_router(profile.router, prefix=API_PREFIX)
app.include_router(history.router, prefix=API_PREFIX)
app.include_router(phrases.router, prefix=API_PREFIX)
