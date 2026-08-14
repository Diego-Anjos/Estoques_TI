"""
Schemas Pydantic para Local
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocalBase(BaseModel):
    """Schema base de local"""
    nome: str = Field(..., min_length=2, max_length=120, description="Nome do local (ex: Prédio A)")
    setor: Optional[str] = Field(None, max_length=80, description="Setor (ex: TI, RH)")
    descricao: Optional[str] = Field(None, max_length=300, description="Descrição do local")
    status: str = Field("Ativo", max_length=20, description="Status: Ativo ou Inativo")


class LocalCreate(LocalBase):
    """Schema para criação de local"""
    pass


class LocalUpdate(BaseModel):
    """Schema para atualização de local"""
    nome: Optional[str] = Field(None, min_length=2, max_length=120)
    setor: Optional[str] = Field(None, max_length=80)
    descricao: Optional[str] = Field(None, max_length=300)
    status: Optional[str] = Field(None, max_length=20)


class LocalResponse(LocalBase):
    """Schema de resposta de local"""
    id_local: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None

    class Config:
        from_attributes = True
