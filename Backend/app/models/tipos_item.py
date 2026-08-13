"""
Model para tabela TIPOS_ITEM
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TipoItem:
    """Representa um tipo de item (PC, MONITOR, CABO_HDMI, etc.)"""
    id_tipo_item: Optional[int] = None
    codigo: str = ""
    nome: str = ""
    serializado: str = "N"  # 'S' ou 'N'
    unidade: str = "UN"
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_tipo_item': self.id_tipo_item,
            'codigo': self.codigo,
            'nome': self.nome,
            'serializado': self.serializado,
            'unidade': self.unidade,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
