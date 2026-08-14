"""
Schemas Pydantic para Item (cadastro de itens com local e quantidade)
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    """Schema para criação de item"""
    nome: str = Field(..., min_length=2, max_length=200, description="Nome do item")
    id_tipo_item: int = Field(..., description="ID do tipo/categoria (FK)")
    descricao: Optional[str] = Field(None, max_length=400, description="Descrição do item")
    quantidade: int = Field(0, ge=0, description="Quantidade em estoque")
    unidade: str = Field("UN", min_length=1, max_length=30, description="Unidade (UN, KG, etc.)")
    id_local: int = Field(..., description="ID do local (FK)")
    status: str = Field("Ativo", max_length=20, description="Status: Ativo ou Inativo")


class ItemUpdate(BaseModel):
    """
    Schema para atualização de item.
    Quantidade é read-only: alterações de saldo só via POST /movimentacoes/.
    """
    nome: Optional[str] = Field(None, min_length=2, max_length=200)
    id_tipo_item: Optional[int] = Field(None, description="ID do tipo/categoria (FK)")
    descricao: Optional[str] = Field(None, max_length=400)
    unidade: Optional[str] = Field(None, min_length=1, max_length=30)
    id_local: Optional[int] = None
    status: Optional[str] = Field(None, max_length=20)


class ItemResponse(BaseModel):
    """Schema de resposta de item"""
    model_config = ConfigDict(from_attributes=True)

    id_item: int
    nome: str
    id_tipo_item: Optional[int] = Field(None, description="ID do tipo/categoria (FK)")
    tipo: Optional[str] = Field(None, description="Nome do tipo/categoria (via join)")
    descricao: Optional[str] = None
    quantidade: int = 0
    unidade: str = "UN"
    id_local: int
    status: str = "Ativo"
    nome_local: Optional[str] = Field(None, description="Nome do local associado")
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
