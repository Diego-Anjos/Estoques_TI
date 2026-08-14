"""
Schemas Pydantic para Movimentações de Estoque
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class MovimentacaoCreate(BaseModel):
    """Request para registrar entrada/saída"""
    id_item: int = Field(..., description="ID do item")
    tipo_movimentacao: str = Field(..., description="Entrada ou Saída")
    quantidade: int = Field(..., gt=0, description="Quantidade movimentada")
    observacao: Optional[str] = Field(None, max_length=300, description="Observação/motivo")
    usuario_id: Optional[int] = Field(None, description="ID do usuário (opcional)")

    @field_validator('tipo_movimentacao')
    @classmethod
    def normalizar_tipo(cls, value: str) -> str:
        raw = (value or '').strip().upper()
        raw = raw.replace('Í', 'I').replace('Á', 'A')
        if raw in ('ENTRADA', 'E'):
            return 'ENTRADA'
        if raw in ('SAIDA', 'SAÍDA', 'S'):
            return 'SAIDA'
        # Aceita labels do front ("entrada" / "saida")
        if raw.startswith('ENTR'):
            return 'ENTRADA'
        if raw.startswith('SAID'):
            return 'SAIDA'
        raise ValueError("tipo_movimentacao deve ser 'Entrada' ou 'Saída'")


class MovimentacaoResponse(BaseModel):
    """Resposta de movimentação com nome do item"""
    id_movimentacao: int
    id_item: int
    nome_item: Optional[str] = None
    tipo_movimentacao: str
    quantidade: int
    observacao: Optional[str] = None
    data_movimentacao: datetime
    usuario_id: Optional[int] = None
    quantidade_atual: Optional[int] = None

    class Config:
        from_attributes = True
