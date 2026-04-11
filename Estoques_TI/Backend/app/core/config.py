"""
Configurações da aplicação carregadas do arquivo .env
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Oracle Database
    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_DSN: str
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


# Instância global das configurações
settings = Settings()
