"""
Model para tabela ESTOQUE_MOVIMENTACOES
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class EstoqueMovimentacao:
    """Representa uma movimentação de estoque (entrada, saída, transferência, ajuste)"""
    id_movimentacao: Optional[int] = None
    id_item: int = 0
    id_local_origem: Optional[int] = None
    id_local_destino: Optional[int] = None
    quantidade: int = 0
    tipo_movimentacao: str = ""  # ENTRADA, SAIDA, TRANSFERENCIA, AJUSTE
    motivo: Optional[str] = None
    documento_ref: Optional[str] = None
    data_criacao: Optional[datetime] = None
    criado_por: int = 0
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_movimentacao': self.id_movimentacao,
            'id_item': self.id_item,
            'id_local_origem': self.id_local_origem,
            'id_local_destino': self.id_local_destino,
            'quantidade': self.quantidade,
            'tipo_movimentacao': self.tipo_movimentacao,
            'motivo': self.motivo,
            'documento_ref': self.documento_ref,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por
        }
