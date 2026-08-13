"""
Model para tabela SOFTWARE_LICENCAS_POOL
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class SoftwareLicencaPool:
    """Representa um pool de licenças de software"""
    id_pool: Optional[int] = None
    id_software: int = 0
    total_licencas: int = 0
    contrato_ref: Optional[str] = None
    data_expiracao: Optional[date] = None
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_pool': self.id_pool,
            'id_software': self.id_software,
            'total_licencas': self.total_licencas,
            'contrato_ref': self.contrato_ref,
            'data_expiracao': self.data_expiracao,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
