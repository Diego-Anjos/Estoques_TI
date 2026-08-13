"""
Schemas Pydantic para Patrimônio
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class StatusPatrimonioEnum(str, Enum):
    """Enum para status do patrimônio"""
    EM_ESTOQUE = "EM_ESTOQUE"
    EM_USO = "EM_USO"
    MANUTENCAO = "MANUTENCAO"
    EXTRAVIADO = "EXTRAVIADO"
    DESCARTADO = "DESCARTADO"


# ========== PATRIMÔNIO ==========

class PatrimonioBase(BaseModel):
    """Schema base de patrimônio"""
    id_item: int = Field(..., description="ID do item (catálogo)")
    numero_serie: Optional[str] = Field(None, max_length=120, description="Número de série")
    numero_patrimonio: Optional[str] = Field(None, max_length=120, description="Número do patrimônio")
    status: StatusPatrimonioEnum = Field(StatusPatrimonioEnum.EM_ESTOQUE, description="Status do patrimônio")
    id_local: int = Field(..., description="ID do local onde está")
    id_usuario_alocado: Optional[int] = Field(None, description="ID do usuário alocado")
    data_compra: Optional[date] = Field(None, description="Data da compra")
    data_fim_garantia: Optional[date] = Field(None, description="Data fim da garantia")
    observacoes: Optional[str] = Field(None, max_length=400, description="Observações")


class PatrimonioCreate(PatrimonioBase):
    """Schema para criação de patrimônio"""
    pass


class PatrimonioUpdate(BaseModel):
    """Schema para atualização de patrimônio"""
    id_item: Optional[int] = None
    numero_serie: Optional[str] = Field(None, max_length=120)
    numero_patrimonio: Optional[str] = Field(None, max_length=120)
    status: Optional[StatusPatrimonioEnum] = None
    id_local: Optional[int] = None
    id_usuario_alocado: Optional[int] = None
    data_compra: Optional[date] = None
    data_fim_garantia: Optional[date] = None
    observacoes: Optional[str] = Field(None, max_length=400)


class PatrimonioResponse(PatrimonioBase):
    """Schema de resposta de patrimônio"""
    id_patrimonio: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== ATRIBUTOS DE PATRIMÔNIO ==========

class PatrimonioAtributoBase(BaseModel):
    """Schema base de atributo de patrimônio"""
    nome_atributo: str = Field(..., max_length=60, description="Nome do atributo (ex: cpu, ram_gb)")
    valor_atributo: str = Field(..., max_length=200, description="Valor do atributo (ex: i5, 16)")


class PatrimonioAtributoCreate(PatrimonioAtributoBase):
    """Schema para criação de atributo"""
    id_patrimonio: int = Field(..., description="ID do patrimônio")


class PatrimonioAtributoResponse(PatrimonioAtributoBase):
    """Schema de resposta de atributo"""
    id_patrimonio: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== SCHEMAS AUXILIARES ==========

class PatrimonioComAtributos(PatrimonioResponse):
    """Patrimônio com seus atributos"""
    atributos: List[PatrimonioAtributoResponse] = []


class AlocarPatrimonioRequest(BaseModel):
    """Request para alocar patrimônio a um usuário"""
    id_usuario_alocado: int
    observacoes: Optional[str] = None


class TransferirPatrimonioRequest(BaseModel):
    """Request para transferir patrimônio de local"""
    id_local_destino: int
    observacoes: Optional[str] = None
