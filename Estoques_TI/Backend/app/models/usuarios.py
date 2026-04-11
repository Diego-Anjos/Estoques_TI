"""
Model para tabela USUARIOS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Usuario:
    """Representa um usuário do sistema"""
    id_usuario: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha_hash: str = ""
    ativo: str = "S"
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_usuario': self.id_usuario,
            'nome': self.nome,
            'email': self.email,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
