"""
Model para tabela ITENS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Item:
    """Representa um item do estoque vinculado a um local"""
    id_item: Optional[int] = None
    nome: str = ""
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    quantidade: int = 0
    unidade: str = "UN"
    id_local: Optional[int] = None
    status: str = "Ativo"
    id_tipo_item: Optional[int] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    estoque_minimo: int = 0
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    nome_local: Optional[str] = None

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_item': self.id_item,
            'nome': self.nome,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'unidade': self.unidade,
            'id_local': self.id_local,
            'status': self.status,
            'id_tipo_item': self.id_tipo_item,
            'marca': self.marca,
            'modelo': self.modelo,
            'estoque_minimo': self.estoque_minimo,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por,
            'nome_local': self.nome_local,
        }
