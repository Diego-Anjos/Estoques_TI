"""
Model para tabela ITENS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Item:
    """Representa um item do catálogo (ex: Teclado Logitech K120, SSD Kingston 480GB)"""
    id_item: Optional[int] = None
    id_tipo_item: int = 0
    nome: str = ""
    marca: Optional[str] = None
    modelo: Optional[str] = None
    descricao: Optional[str] = None
    estoque_minimo: int = 0
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_item': self.id_item,
            'id_tipo_item': self.id_tipo_item,
            'nome': self.nome,
            'marca': self.marca,
            'modelo': self.modelo,
            'descricao': self.descricao,
            'estoque_minimo': self.estoque_minimo,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
