"""
Model para tabela SOFTWARE_ATRIBUICOES
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class SoftwareAtribuicao:
    """Representa a atribuição de uma licença a um usuário ou patrimônio"""
    id_atribuicao: Optional[int] = None
    id_pool: int = 0
    id_usuario: Optional[int] = None
    id_patrimonio: Optional[int] = None
    data_atribuicao: date = None
    data_remocao: Optional[date] = None
    observacoes: Optional[str] = None
    data_criacao: Optional[datetime] = None
    criado_por: int = 0
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_atribuicao': self.id_atribuicao,
            'id_pool': self.id_pool,
            'id_usuario': self.id_usuario,
            'id_patrimonio': self.id_patrimonio,
            'data_atribuicao': self.data_atribuicao,
            'data_remocao': self.data_remocao,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por
        }
