"""
Model para tabela TIPOS_ITEM
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TipoItem:
    """Representa um tipo/categoria de item do estoque"""
    id_tipo_item: Optional[int] = None
    nome: str = ""
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    status: str = "Ativo"
    codigo: Optional[str] = None
    serializado: str = "N"
    unidade: str = "UN"
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    nome_criado_por: Optional[str] = None

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_tipo_item': self.id_tipo_item,
            'nome': self.nome,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'status': self.status,
            'codigo': self.codigo,
            'serializado': self.serializado,
            'unidade': self.unidade,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por,
            'nome_criado_por': self.nome_criado_por,
        }
