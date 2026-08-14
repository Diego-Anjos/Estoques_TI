"""
Schemas Pydantic para Movimentações de Estoque
"""
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime


def normalizar_tipo_movimentacao(value: str) -> str:
    """
    Converte qualquer variação vinda da UI ('Entrada', 'saída', 'D', 'Devolução')
    no valor gravado na coluna TIPO_MOVIMENTACAO:
    'ENTRADA' | 'SAIDA' | 'DEVOLUCAO'
    """
    raw = (value or '').strip().upper()
    raw = (
        raw.replace('Í', 'I')
        .replace('Á', 'A')
        .replace('É', 'E')
        .replace('Ó', 'O')
        .replace('Ú', 'U')
        .replace('Ç', 'C')
    )
    if raw in ('ENTRADA', 'E'):
        return 'ENTRADA'
    if raw in ('SAIDA', 'S'):
        return 'SAIDA'
    if raw in ('DEVOLUCAO', 'D'):
        return 'DEVOLUCAO'
    if raw.startswith('ENTR'):
        return 'ENTRADA'
    if raw.startswith('SAID'):
        return 'SAIDA'
    if raw.startswith('DEVOL'):
        return 'DEVOLUCAO'
    raise ValueError("tipo_movimentacao deve ser 'Entrada', 'Saída' ou 'Devolução'")


def _limpar_setor(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    limpo = value.strip()
    return limpo or None


class MovimentacaoCreate(BaseModel):
    """Request para registrar entrada/saída/devolução"""
    id_item: int = Field(..., description="ID do item")
    tipo_movimentacao: str = Field(..., description="Entrada, Saída ou Devolução")
    quantidade: int = Field(..., gt=0, description="Quantidade movimentada")
    observacao: Optional[str] = Field(None, max_length=300, description="Observação/motivo")
    setor_destino: Optional[str] = Field(
        None,
        max_length=80,
        description="Setor/departamento de destino (saídas)",
    )
    setor_origem: Optional[str] = Field(
        None,
        max_length=80,
        description="Setor de onde o item está retornando (devoluções)",
    )
    usuario_id: Optional[int] = Field(None, description="ID do usuário (opcional)")

    @field_validator('tipo_movimentacao')
    @classmethod
    def normalizar_tipo(cls, value: str) -> str:
        return normalizar_tipo_movimentacao(value)

    @field_validator('setor_destino', 'setor_origem')
    @classmethod
    def limpar_setores(cls, value: Optional[str]) -> Optional[str]:
        return _limpar_setor(value)


class MovimentacaoResponse(BaseModel):
    """
    Resposta de movimentação com dados do item (nome/saldo via JOIN).
    Aceita dict do repositório ou dataclass EstoqueMovimentacao (from_attributes).
    """
    model_config = ConfigDict(from_attributes=True)

    id_movimentacao: int
    id_item: int
    nome_item: Optional[str] = None
    tipo_movimentacao: str
    quantidade: int
    observacao: Optional[str] = None
    setor_destino: Optional[str] = None
    setor_origem: Optional[str] = None
    data_movimentacao: datetime
    usuario_id: Optional[int] = None
    quantidade_atual: Optional[int] = None

    @field_validator('quantidade', 'quantidade_atual', 'id_movimentacao', 'id_item', mode='before')
    @classmethod
    def coercer_numeros(cls, value):
        """Oracle NUMBER / Decimal → int (evita falha de serialização)."""
        if value is None:
            return value
        return int(value)
