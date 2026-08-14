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


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Oracle Database (opcionais para permitir boot sem credenciais no Render)
    ORACLE_USER: Optional[str] = None
    ORACLE_PASSWORD: Optional[str] = None
    ORACLE_DSN: Optional[str] = None
    ORACLE_POOL_MIN: int = 1
    ORACLE_POOL_MAX: int = 5
    ORACLE_POOL_INC: int = 1

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

    @property
    def oracle_configured(self) -> bool:
        """Indica se as credenciais Oracle obrigatórias estão definidas."""
        return bool(self.ORACLE_USER and self.ORACLE_PASSWORD and self.ORACLE_DSN)


def _load_settings() -> Settings:
    """
    Carrega settings do .env.
    JWT_SECRET_KEY inválida/ausente aborta a inicialização com erro claro.
    Falhas só de Oracle geram warning (banco pode ficar indisponível).
    """
    try:
        loaded = Settings()
    except Exception as exc:
        message = str(exc)
        # Falha de JWT: abortar com mensagem no terminal
        if "JWT_SECRET_KEY" in message or "jwt" in message.lower():
            print(message, file=sys.stderr)
            raise SystemExit(1) from exc

        # Outras falhas de parse: também não engolir JWT se vier aninhado
        print(
            f"\nFalha ao carregar configurações: {exc}\n"
            "Verifique o arquivo Backend/.env (incluindo JWT_SECRET_KEY).\n",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    if not loaded.oracle_configured:
        logger.warning(
            "Variáveis Oracle (ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN) "
            "não configuradas. A API subirá, mas o banco ficará indisponível."
        )
    return loaded


# Instância global das configurações
settings = _load_settings()
