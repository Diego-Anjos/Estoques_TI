"""
Model para tabela SOFTWARES
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Software:
    """Representa um software (ex: Microsoft Office, CoopSys)"""
    id_software: Optional[int] = None
    nome: str = ""
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_software': self.id_software,
            'nome': self.nome,
            'fabricante': self.fabricante,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
