"""
Schemas Pydantic para Ocorrência
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SeveridadeEnum(str, Enum):
    """Enum para severidade da ocorrência"""
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"


class StatusOcorrenciaEnum(str, Enum):
    """Enum para status da ocorrência"""
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    RESOLVIDA = "RESOLVIDA"
    FECHADA = "FECHADA"


class OcorrenciaBase(BaseModel):
    """Schema base de ocorrência"""
    titulo: str = Field(..., min_length=5, max_length=200, description="Título da ocorrência")
    descricao: Optional[str] = Field(None, max_length=2000, description="Descrição detalhada")
    severidade: SeveridadeEnum = Field(SeveridadeEnum.MEDIA, description="Severidade")
    id_usuario_solicitante: int = Field(..., description="ID do usuário solicitante")
    id_usuario_relacionado: Optional[int] = Field(None, description="ID do usuário relacionado")
    id_patrimonio_relacionado: Optional[int] = Field(None, description="ID do patrimônio relacionado")


class OcorrenciaCreate(OcorrenciaBase):
    """Schema para criação de ocorrência"""
    pass


class OcorrenciaUpdate(BaseModel):
    """Schema para atualização de ocorrência"""
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    descricao: Optional[str] = Field(None, max_length=2000)
    severidade: Optional[SeveridadeEnum] = None
    status: Optional[StatusOcorrenciaEnum] = None
    id_usuario_relacionado: Optional[int] = None
    id_patrimonio_relacionado: Optional[int] = None


class OcorrenciaResponse(OcorrenciaBase):
    """Schema de resposta de ocorrência"""
    id_ocorrencia: int
    status: StatusOcorrenciaEnum
    id_usuario_abriu: int
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== SCHEMAS AUXILIARES ==========

class FecharOcorrenciaRequest(BaseModel):
    """Request para fechar uma ocorrência"""
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações de fechamento")


class AlterarStatusRequest(BaseModel):
    """Request para alterar status da ocorrência"""
    status: StatusOcorrenciaEnum
    observacoes: Optional[str] = Field(None, max_length=500)
