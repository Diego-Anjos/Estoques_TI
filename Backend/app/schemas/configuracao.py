"""
Schemas Pydantic para Configurações do Sistema
"""
from pydantic import BaseModel, Field
from typing import Optional


class ConfiguracaoResponse(BaseModel):
    id_config: int = 1
    nome_empresa: str = "Controle de Estoque"
    modo_escuro: bool = False
    alerta_estoque_minimo: int = Field(5, ge=0)

    class Config:
        from_attributes = True


class ConfiguracaoUpdate(BaseModel):
    nome_empresa: Optional[str] = Field(None, min_length=2, max_length=150)
    modo_escuro: Optional[bool] = None
    alerta_estoque_minimo: Optional[int] = Field(None, ge=0)
