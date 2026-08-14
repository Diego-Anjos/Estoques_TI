"""
Model para tabela ESTOQUES_TI_MOVIMENTACOES
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class EstoqueMovimentacao:
    """Representa uma movimentação de estoque (entrada/saída/devolução)"""
    id_movimentacao: Optional[int] = None
    id_item: int = 0
    id_local_origem: Optional[int] = None
    id_local_destino: Optional[int] = None
    quantidade: int = 0
    tipo_movimentacao: str = ""  # ENTRADA | SAIDA | DEVOLUCAO
    observacao: Optional[str] = None
    setor_destino: Optional[str] = None
    setor_origem: Optional[str] = None
    data_movimentacao: Optional[datetime] = None
    usuario_id: Optional[int] = None
    nome_item: Optional[str] = None
    quantidade_atual: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            'id_movimentacao': self.id_movimentacao,
            'id_item': self.id_item,
            'id_local_origem': self.id_local_origem,
            'id_local_destino': self.id_local_destino,
            'quantidade': self.quantidade,
            'tipo_movimentacao': self.tipo_movimentacao,
            'observacao': self.observacao,
            'setor_destino': self.setor_destino,
            'setor_origem': self.setor_origem,
            'data_movimentacao': self.data_movimentacao,
            'usuario_id': self.usuario_id,
            'nome_item': self.nome_item,
            'quantidade_atual': self.quantidade_atual,
        }
