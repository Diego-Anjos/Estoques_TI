"""
Schemas Pydantic para Item (cadastro de itens com local e quantidade)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Schema base de item"""
    nome: str = Field(..., min_length=2, max_length=200, description="Nome do item")
    tipo: Optional[str] = Field(None, max_length=120, description="Tipo/categoria do item")
    descricao: Optional[str] = Field(None, max_length=400, description="Descrição do item")
    quantidade: int = Field(0, ge=0, description="Quantidade em estoque")
    unidade: str = Field("UN", min_length=1, max_length=30, description="Unidade (UN, KG, etc.)")
    id_local: int = Field(..., description="ID do local (FK)")
    status: str = Field("Ativo", max_length=20, description="Status: Ativo ou Inativo")


class ItemCreate(ItemBase):
    """Schema para criação de item"""
    pass


class ItemUpdate(BaseModel):
    """Schema para atualização de item"""
    nome: Optional[str] = Field(None, min_length=2, max_length=200)
    tipo: Optional[str] = Field(None, max_length=120)
    descricao: Optional[str] = Field(None, max_length=400)
    quantidade: Optional[int] = Field(None, ge=0)
    unidade: Optional[str] = Field(None, min_length=1, max_length=30)
    id_local: Optional[int] = None
    status: Optional[str] = Field(None, max_length=20)


class ItemResponse(ItemBase):
    """Schema de resposta de item"""
    id_item: int
    nome_local: Optional[str] = Field(None, description="Nome do local associado")
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None

    class Config:
        from_attributes = True
