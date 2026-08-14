"""
Schemas Pydantic para Tipo de Item
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TipoItemBase(BaseModel):
    """Schema base de tipo de item (categoria: Hardware, Periféricos, Redes, etc.)"""
    nome: str = Field(..., min_length=2, max_length=120, description="Nome da categoria/tipo (ex: Hardware)")
    categoria: Optional[str] = Field(None, max_length=80, description="Campo legado (opcional)")
    descricao: Optional[str] = Field(None, max_length=400, description="Descrição do tipo")
    status: str = Field("Ativo", max_length=20, description="Status: Ativo ou Inativo")


class TipoItemCreate(TipoItemBase):
    """Schema para criação de tipo de item"""
    pass


class TipoItemUpdate(BaseModel):
    """Schema para atualização de tipo de item"""
    nome: Optional[str] = Field(None, min_length=2, max_length=120)
    categoria: Optional[str] = Field(None, max_length=80)
    descricao: Optional[str] = Field(None, max_length=400)
    status: Optional[str] = Field(None, max_length=20)


class TipoItemResponse(TipoItemBase):
    """Schema de resposta de tipo de item"""
    id_tipo_item: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    nome_criado_por: Optional[str] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None

    class Config:
        from_attributes = True
