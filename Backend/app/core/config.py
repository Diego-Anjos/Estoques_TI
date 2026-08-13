"""
Configurações da aplicação carregadas do arquivo .env
"""
import logging
from typing import Optional

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


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

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def oracle_configured(self) -> bool:
        """Indica se as credenciais Oracle obrigatórias estão definidas."""
        return bool(self.ORACLE_USER and self.ORACLE_PASSWORD and self.ORACLE_DSN)


def _load_settings() -> Settings:
    """Carrega settings sem derrubar o processo se algo falhar na leitura."""
    try:
        loaded = Settings()
        if not loaded.oracle_configured:
            logger.warning(
                "Variáveis Oracle (ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN) "
                "não configuradas. A API subirá, mas o banco ficará indisponível."
            )
        return loaded
    except Exception as exc:
        logger.warning(
            "Falha ao carregar configurações (%s). Usando defaults sem Oracle.",
            exc,
        )
        return Settings(
            ORACLE_USER=None,
            ORACLE_PASSWORD=None,
            ORACLE_DSN=None,
        )


# Instância global das configurações
settings = _load_settings()
