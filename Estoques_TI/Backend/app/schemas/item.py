"""
Schemas Pydantic para Item (catálogo de itens)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Schema base de item"""
    id_tipo_item: int = Field(..., description="ID do tipo de item")
    nome: str = Field(..., min_length=3, max_length=200, description="Nome do item")
    marca: Optional[str] = Field(None, max_length=120, description="Marca do item")
    modelo: Optional[str] = Field(None, max_length=120, description="Modelo do item")
    descricao: Optional[str] = Field(None, max_length=400, description="Descrição do item")
    estoque_minimo: int = Field(0, ge=0, description="Estoque mínimo")


class ItemCreate(ItemBase):
    """Schema para criação de item"""
    pass


class ItemUpdate(BaseModel):
    """Schema para atualização de item"""
    id_tipo_item: Optional[int] = None
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    marca: Optional[str] = Field(None, max_length=120)
    modelo: Optional[str] = Field(None, max_length=120)
    descricao: Optional[str] = Field(None, max_length=400)
    estoque_minimo: Optional[int] = Field(None, ge=0)


class ItemResponse(ItemBase):
    """Schema de resposta de item"""
    id_item: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True
