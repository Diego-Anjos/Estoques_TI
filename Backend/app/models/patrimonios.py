"""
Model para tabela PATRIMONIOS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Patrimonio:
    """Representa um patrimônio (item serializado: PC, Notebook, Monitor, etc.)"""
    id_patrimonio: Optional[int] = None
    id_item: int = 0
    numero_serie: Optional[str] = None
    numero_patrimonio: Optional[str] = None
    status: str = "EM_ESTOQUE"  # EM_ESTOQUE, EM_USO, MANUTENCAO, EXTRAVIADO, DESCARTADO
    id_local: int = 0
    id_usuario_alocado: Optional[int] = None
    data_compra: Optional[date] = None
    data_fim_garantia: Optional[date] = None
    observacoes: Optional[str] = None
    data_criacao: Optional[datetime] = None
    criado_por: Optional[int] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_patrimonio': self.id_patrimonio,
            'id_item': self.id_item,
            'numero_serie': self.numero_serie,
            'numero_patrimonio': self.numero_patrimonio,
            'status': self.status,
            'id_local': self.id_local,
            'id_usuario_alocado': self.id_usuario_alocado,
            'data_compra': self.data_compra,
            'data_fim_garantia': self.data_fim_garantia,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao,
            'criado_por': self.criado_por,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
