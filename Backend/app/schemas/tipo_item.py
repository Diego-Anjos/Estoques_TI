"""
Schemas Pydantic para Tipo de Item
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SerializadoEnum(str, Enum):
    """Enum para campo serializado"""
    SIM = "S"
    NAO = "N"


class TipoItemBase(BaseModel):
    """Schema base de tipo de item"""
    codigo: str = Field(..., min_length=2, max_length=40, description="Código do tipo (ex: PC, MONITOR)")
    nome: str = Field(..., min_length=3, max_length=120, description="Nome do tipo")
    serializado: SerializadoEnum = Field(SerializadoEnum.NAO, description="Item é serializado? (S/N)")
    unidade: str = Field("UN", max_length=30, description="Unidade de medida")


class TipoItemCreate(TipoItemBase):
    """Schema para criação de tipo de item"""
    pass


class TipoItemUpdate(BaseModel):
    """Schema para atualização de tipo de item"""
    codigo: Optional[str] = Field(None, min_length=2, max_length=40)
    nome: Optional[str] = Field(None, min_length=3, max_length=120)
    serializado: Optional[SerializadoEnum] = None
    unidade: Optional[str] = Field(None, max_length=30)


class TipoItemResponse(TipoItemBase):
    """Schema de resposta de tipo de item"""
    id_tipo_item: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True
