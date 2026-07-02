"""Configuracion centralizada del sistema via pydantic-settings.

Todas las variables se leen de entorno o de un archivo `.env` en la raiz
del repo. Nunca se hardcodean credenciales ni IDs de modelo versionados:
los alias de modelo viven en `config/model_assignment.yaml`.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Configuracion de runtime del sistema agentico de procurement."""

    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Base de datos (data spine)
    database_url: str = Field(
        default="postgresql+psycopg://procurement:procurement@localhost:5432/procurement",
        description="URL de conexion SQLAlchemy (driver psycopg v3) a Postgres.",
    )

    # Claude Agent SDK / Anthropic
    # Opcional en tiempo de import: el sistema debe poder importarse (para
    # generar datos sinteticos, correr migraciones, tests unitarios, etc.)
    # sin que la clave este presente. Solo se exige al invocar al SDK.
    anthropic_api_key: str | None = Field(default=None)

    # Observabilidad (OpenTelemetry -> Arize Phoenix)
    otel_exporter_otlp_endpoint: str = Field(default="http://localhost:4318")
    phoenix_ui_url: str = Field(default="http://localhost:6006")
    otel_service_name: str = Field(default="procurement-agents")

    # Umbrales de negocio por defecto (guardrails). Los agentes concretos
    # pueden sobreescribirlos via `guardrails/policies/*.yaml`.
    default_confidence_threshold: float = Field(
        default=0.7, description="Confianza minima para no degradar a needs_review."
    )
    default_savings_limit_usd: float = Field(
        default=250_000.0,
        description="Ahorro reportado por encima del cual se exige needs_review.",
    )

    # Rutas de configuracion declarativa
    model_assignment_path: Path = Field(
        default=REPO_ROOT
        / "src"
        / "procurement_agents"
        / "config"
        / "model_assignment.yaml"
    )
    agent_registry_path: Path = Field(
        default=REPO_ROOT / "src" / "procurement_agents" / "agents" / "registry.yaml"
    )

    # Entorno de ejecucion
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    def require_anthropic_api_key(self) -> str:
        """Devuelve la API key o lanza un error claro si falta.

        Se usa justo antes de invocar al Claude Agent SDK, nunca en import.
        """
        if not self.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY no esta configurada. Definela en el entorno "
                "o en el archivo .env antes de invocar a los agentes."
            )
        return self.anthropic_api_key


@lru_cache
def get_settings() -> Settings:
    """Devuelve una instancia cacheada de `Settings`."""
    return Settings()
