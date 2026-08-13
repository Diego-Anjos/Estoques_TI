"""
Schemas Pydantic para Estoque (Saldo e Movimentações)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoMovimentacaoEnum(str, Enum):
    """Enum para tipo de movimentação"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    TRANSFERENCIA = "TRANSFERENCIA"
    AJUSTE = "AJUSTE"


# ========== ESTOQUE SALDO ==========

class EstoqueSaldoBase(BaseModel):
    """Schema base de saldo de estoque"""
    id_item: int = Field(..., description="ID do item")
    id_local: int = Field(..., description="ID do local")
    quantidade: int = Field(0, ge=0, description="Quantidade em estoque")


class EstoqueSaldoResponse(EstoqueSaldoBase):
    """Schema de resposta de saldo de estoque"""
    data_alteracao: datetime
    alterado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


# ========== ESTOQUE MOVIMENTAÇÕES ==========

class EstoqueMovimentacaoBase(BaseModel):
    """Schema base de movimentação de estoque"""
    id_item: int = Field(..., description="ID do item")
    quantidade: int = Field(..., gt=0, description="Quantidade movimentada")
    tipo_movimentacao: TipoMovimentacaoEnum = Field(..., description="Tipo de movimentação")
    motivo: Optional[str] = Field(None, max_length=300, description="Motivo da movimentação")
    documento_ref: Optional[str] = Field(None, max_length=80, description="Documento de referência")


class EstoqueMovimentacaoCreate(EstoqueMovimentacaoBase):
    """Schema para criação de movimentação"""
    id_local_origem: Optional[int] = Field(None, description="ID do local de origem")
    id_local_destino: Optional[int] = Field(None, description="ID do local de destino")


class EstoqueMovimentacaoResponse(EstoqueMovimentacaoBase):
    """Schema de resposta de movimentação"""
    id_movimentacao: int
    id_local_origem: Optional[int] = None
    id_local_destino: Optional[int] = None
    data_criacao: datetime
    criado_por: int
    
    class Config:
        from_attributes = True


# ========== SCHEMAS AUXILIARES ==========

class MovimentacaoEntradaRequest(BaseModel):
    """Request para entrada de estoque"""
    id_item: int
    id_local_destino: int
    quantidade: int = Field(..., gt=0)
    motivo: Optional[str] = None
    documento_ref: Optional[str] = None


class MovimentacaoSaidaRequest(BaseModel):
    """Request para saída de estoque"""
    id_item: int
    id_local_origem: int
    quantidade: int = Field(..., gt=0)
    motivo: Optional[str] = None
    documento_ref: Optional[str] = None


class MovimentacaoTransferenciaRequest(BaseModel):
    """Request para transferência entre locais"""
    id_item: int
    id_local_origem: int
    id_local_destino: int
    quantidade: int = Field(..., gt=0)
    motivo: Optional[str] = None
    documento_ref: Optional[str] = None
