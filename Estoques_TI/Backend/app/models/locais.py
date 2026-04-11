"""
Model para tabela LOCAIS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Local:
    """Representa um local físico (almoxarifado, sala, setor, etc.)"""
    id_local: Optional[int] = None
    nome: str = ""
    descricao: Optional[str] = None
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_local': self.id_local,
            'nome': self.nome,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
