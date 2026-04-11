"""
Model para tabela ESTOQUE_SALDO
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class EstoqueSaldo:
    """Representa o saldo de estoque de itens não serializados"""
    id_item: int = 0
    id_local: int = 0
    quantidade: int = 0
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_item': self.id_item,
            'id_local': self.id_local,
            'quantidade': self.quantidade,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
