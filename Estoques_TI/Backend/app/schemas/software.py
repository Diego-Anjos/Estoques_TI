"""
Schemas Pydantic para Software e Licenças
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


# ========== SOFTWARE ==========

class SoftwareBase(BaseModel):
    """Schema base de software"""
    nome: str = Field(..., min_length=3, max_length=120, description="Nome do software")
    fabricante: Optional[str] = Field(None, max_length=120, description="Fabricante")
    descricao: Optional[str] = Field(None, max_length=300, description="Descrição")


class SoftwareCreate(SoftwareBase):
    """Schema para criação de software"""
    pass


class SoftwareUpdate(BaseModel):
    """Schema para atualização de software"""
    nome: Optional[str] = Field(None, min_length=3, max_length=120)
    fabricante: Optional[str] = Field(None, max_length=120)
    descricao: Optional[str] = Field(None, max_length=300)


class SoftwareResponse(SoftwareBase):
    """Schema de resposta de software"""
    id_software: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== POOL DE LICENÇAS ==========

class SoftwareLicencaPoolBase(BaseModel):
    """Schema base de pool de licenças"""
    id_software: int = Field(..., description="ID do software")
    total_licencas: int = Field(..., ge=0, description="Total de licenças disponíveis")
    contrato_ref: Optional[str] = Field(None, max_length=100, description="Referência do contrato")
    data_expiracao: Optional[date] = Field(None, description="Data de expiração")


class SoftwareLicencaPoolCreate(SoftwareLicencaPoolBase):
    """Schema para criação de pool de licenças"""
    pass


class SoftwareLicencaPoolUpdate(BaseModel):
    """Schema para atualização de pool de licenças"""
    id_software: Optional[int] = None
    total_licencas: Optional[int] = Field(None, ge=0)
    contrato_ref: Optional[str] = Field(None, max_length=100)
    data_expiracao: Optional[date] = None


class SoftwareLicencaPoolResponse(SoftwareLicencaPoolBase):
    """Schema de resposta de pool de licenças"""
    id_pool: int
    data_criacao: datetime
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== ATRIBUIÇÕES DE LICENÇA ==========

class SoftwareAtribuicaoBase(BaseModel):
    """Schema base de atribuição de licença"""
    id_pool: int = Field(..., description="ID do pool de licenças")
    id_usuario: Optional[int] = Field(None, description="ID do usuário (se atribuído a usuário)")
    id_patrimonio: Optional[int] = Field(None, description="ID do patrimônio (se atribuído a máquina)")
    data_atribuicao: date = Field(..., description="Data da atribuição")
    data_remocao: Optional[date] = Field(None, description="Data da remoção")
    observacoes: Optional[str] = Field(None, max_length=300, description="Observações")


class SoftwareAtribuicaoCreate(BaseModel):
    """Schema para criação de atribuição"""
    id_pool: int
    id_usuario: Optional[int] = None
    id_patrimonio: Optional[int] = None
    observacoes: Optional[str] = Field(None, max_length=300)


class SoftwareAtribuicaoUpdate(BaseModel):
    """Schema para atualização de atribuição"""
    data_remocao: Optional[date] = None
    observacoes: Optional[str] = Field(None, max_length=300)


class SoftwareAtribuicaoResponse(SoftwareAtribuicaoBase):
    """Schema de resposta de atribuição"""
    id_atribuicao: int
    data_criacao: datetime
    criado_por: int
    
    class Config:
        from_attributes = True


# ========== SCHEMAS AUXILIARES ==========

class LicencasDisponiveisResponse(BaseModel):
    """Resposta com informações de licenças disponíveis"""
    id_pool: int
    id_software: int
    nome_software: str
    total_licencas: int
    licencas_em_uso: int
    licencas_disponiveis: int
    data_expiracao: Optional[date] = None
