"""
Schemas Pydantic para Usuário
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Schema base de usuário"""
    nome: str = Field(..., min_length=3, max_length=150, description="Nome do usuário")
    email: EmailStr = Field(..., max_length=200, description="Email do usuário")
    cargo: Optional[str] = Field(None, max_length=100, description="Cargo / job title")


class UsuarioCreate(UsuarioBase):
    """Schema para criação de usuário"""
    senha: str = Field(..., min_length=6, max_length=100, description="Senha do usuário")
    ativo: Optional[str] = Field("S", pattern="^[SN]$", description="Usuário ativo (S/N)")


class UsuarioUpdate(BaseModel):
    """Schema para atualização parcial de usuário"""
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=200)
    cargo: Optional[str] = Field(None, max_length=100)
    senha: Optional[str] = Field(None, min_length=6, max_length=100)
    ativo: Optional[str] = Field(None, pattern="^[SN]$")


class UsuarioResponse(UsuarioBase):
    """Schema de resposta de usuário"""
    id_usuario: int
    ativo: str
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str


class UsuarioLoginResponse(BaseModel):
    """Schema de resposta do login"""
    id_usuario: int
    nome: str
    email: str
    cargo: Optional[str] = None
    mensagem: str = "Login realizado com sucesso"
