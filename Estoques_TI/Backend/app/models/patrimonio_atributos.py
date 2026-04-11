"""
Model para tabela PATRIMONIO_ATRIBUTOS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class PatrimonioAtributo:
    """Representa atributos flexíveis de um patrimônio (ex: cpu=i5, ram_gb=16, ssd_gb=480)"""
    id_patrimonio: int = 0
    nome_atributo: str = ""
    valor_atributo: str = ""
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_patrimonio': self.id_patrimonio,
            'nome_atributo': self.nome_atributo,
            'valor_atributo': self.valor_atributo,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por
        }
