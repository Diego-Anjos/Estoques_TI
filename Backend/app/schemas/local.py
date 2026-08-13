"""
Schemas Pydantic para Local
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocalBase(BaseModel):
    """Schema base de local"""
    nome: str = Field(..., min_length=3, max_length=120, description="Nome do local")
    descricao: Optional[str] = Field(None, max_length=300, description="Descrição do local")


class LocalCreate(LocalBase):
    """Schema para criação de local"""
    pass


class LocalUpdate(BaseModel):
    """Schema para atualização de local"""
    nome: Optional[str] = Field(None, min_length=3, max_length=120)
    descricao: Optional[str] = Field(None, max_length=300)


class LocalResponse(LocalBase):
    """Schema de resposta de local"""
    id_local: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True
