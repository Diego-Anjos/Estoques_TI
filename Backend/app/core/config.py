"""
Configurações da aplicação carregadas do arquivo .env
"""
import logging
import sys
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# Valores que NÃO podem ser usados em produção / desenvolvimento
_INSECURE_JWT_SECRETS = frozenset(
    {
        "",
        "change-me-in-production",
        "troque-esta-chave-por-uma-secreta-longa",
    }
)

_JWT_MISSING_MSG = (
    "\n"
    "============================================================\n"
    "  ERRO DE CONFIGURAÇÃO: JWT_SECRET_KEY não definida\n"
    "============================================================\n"
    "  Defina JWT_SECRET_KEY no arquivo Backend/.env\n"
    "  (veja Backend/.env.example).\n"
    "  A API não pode iniciar sem uma chave JWT segura.\n"
    "============================================================\n"
)

_JWT_INSECURE_MSG = (
    "\n"
    "============================================================\n"
    "  ERRO DE CONFIGURAÇÃO: JWT_SECRET_KEY insegura/padrão\n"
    "============================================================\n"
    "  O valor atual de JWT_SECRET_KEY é um placeholder.\n"
    "  Substitua no Backend/.env por uma chave secreta forte\n"
    "  (ex.: string longa e aleatória).\n"
    "  A API não pode iniciar com o valor padrão.\n"
    "============================================================\n"
)


def validate_jwt_secret_key(secret: Optional[str]) -> str:
    """
    Exige JWT_SECRET_KEY do ambiente/.env.
    Levanta ValueError com mensagem clara se ausente ou insegura.
    """
    if secret is None or not str(secret).strip():
        raise ValueError(_JWT_MISSING_MSG)

    normalized = str(secret).strip()
    if normalized in _INSECURE_JWT_SECRETS:
        raise ValueError(_JWT_INSECURE_MSG)

    return normalized


def normalize_database_url(url: str) -> str:
    """
    SQLAlchemy exige o dialeto 'postgresql://'.
    URLs do Heroku/Supabase às vezes vêm como 'postgres://'.
    """
    normalized = (url or "").strip()
    if normalized.startswith("postgres://"):
        normalized = "postgresql://" + normalized[len("postgres://") :]
    return normalized


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # PostgreSQL (Supabase / local) — obrigatório
    DATABASE_URL: str = Field(..., description="URL de conexão PostgreSQL")

    # API
    API_TITLE: str = "Estoque TI API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # JWT — obrigatório via .env (sem default inseguro)
    JWT_SECRET_KEY: str = Field(..., description="Chave secreta JWT (obrigatória no .env)")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def jwt_secret_must_be_secure(cls, value: str) -> str:
        return validate_jwt_secret_key(value)

    @field_validator("DATABASE_URL")
    @classmethod
    def database_url_must_be_set(cls, value: str) -> str:
        if not value or not str(value).strip():
            raise ValueError(
                "DATABASE_URL não definida. Configure no Backend/.env "
                "(veja Backend/.env.example)."
            )
        return normalize_database_url(value)

    @property
    def database_configured(self) -> bool:
        """Indica se DATABASE_URL está definida."""
        return bool(self.DATABASE_URL and self.DATABASE_URL.strip())


def _load_settings() -> Settings:
    """
    Carrega settings do .env.
    JWT_SECRET_KEY ou DATABASE_URL inválidas abortam a inicialização.
    """
    try:
        loaded = Settings()
    except Exception as exc:
        message = str(exc)
        if "JWT_SECRET_KEY" in message or "jwt" in message.lower():
            print(message, file=sys.stderr)
            raise SystemExit(1) from exc

        if "DATABASE_URL" in message:
            print(
                f"\nFalha ao carregar DATABASE_URL: {exc}\n"
                "Defina DATABASE_URL no Backend/.env (PostgreSQL/Supabase).\n",
                file=sys.stderr,
            )
            raise SystemExit(1) from exc

        print(
            f"\nFalha ao carregar configurações: {exc}\n"
            "Verifique o arquivo Backend/.env (incluindo JWT_SECRET_KEY e DATABASE_URL).\n",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    return loaded


# Instância global das configurações
settings = _load_settings()
