"""Modelos ORM y motor de base de datos (FASE 8)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# --- Tablas (esquema de la FASE 8) ---


class Usuario(Base):
    """
    Perfil del usuario. FASE 8 asume un unico usuario (id fijo = 1);
    la autenticacion y multi-usuario son fases posteriores.
    """

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(255))


class Frase(Base):
    """Frase rapida. Las senas LSP asociadas NO estan validadas (`es_demo`)."""

    __tablename__ = "frases"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    texto: Mapped[str] = mapped_column(String(200))
    categoria: Mapped[str] = mapped_column(String(20), index=True)
    orden: Mapped[int] = mapped_column(default=0)
    es_demo: Mapped[bool] = mapped_column(default=True)


class HistorialTraduccion(Base):
    __tablename__ = "historial_traduccion"

    id: Mapped[str] = mapped_column(String(12), primary_key=True)
    direccion: Mapped[str] = mapped_column(String(20))  # sign-to-text | text-to-sign
    texto: Mapped[str] = mapped_column(String(500))
    es_demo: Mapped[bool] = mapped_column(default=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, index=True
    )


# --- Motor y sesiones ---

_engine = None
_SessionLocal: sessionmaker[Session] | None = None


def init_engine() -> bool:
    """
    Crea el engine y verifica la conexion. Devuelve True si PostgreSQL
    responde; False si hay que caer a memoria.
    """
    global _engine, _SessionLocal

    url = settings.database_url.strip()
    if not url:
        return False

    try:
        _engine = create_engine(url, pool_pre_ping=True, future=True)
        with _engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        _SessionLocal = sessionmaker(
            bind=_engine, autoflush=False, expire_on_commit=False
        )
        return True
    except Exception:
        _engine = None
        _SessionLocal = None
        return False


def create_all() -> None:
    """Crea las tablas si no existen (para desarrollo / tests sin Alembic)."""
    if _engine is not None:
        Base.metadata.create_all(_engine)


def get_session() -> Session:
    if _SessionLocal is None:
        raise RuntimeError("La base de datos no esta inicializada")
    return _SessionLocal()
