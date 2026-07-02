"""Engine y session factory del data spine, construidos desde `Settings`."""
from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from procurement_agents.config.settings import get_settings


@lru_cache
def get_engine() -> Engine:
    """Crea (una unica vez) el engine SQLAlchemy hacia Postgres."""
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True, future=True)


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    """Devuelve el `sessionmaker` cacheado ligado al engine actual."""
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Context manager transaccional: commit al salir, rollback si falla."""
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
