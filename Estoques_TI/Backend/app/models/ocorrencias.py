"""
Model para tabela OCORRENCIAS
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Ocorrencia:
    """Representa uma ocorrência/chamado do sistema"""
    id_ocorrencia: Optional[int] = None
    titulo: str = ""
    descricao: Optional[str] = None
    severidade: str = "MEDIA"  # BAIXA, MEDIA, ALTA, CRITICA
    status: str = "ABERTA"  # ABERTA, EM_ANDAMENTO, RESOLVIDA, FECHADA
    id_usuario_abriu: int = 0
    id_usuario_solicitante: int = 0
    id_usuario_relacionado: Optional[int] = None
    id_patrimonio_relacionado: Optional[int] = None
    data_abertura: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    alterado_por: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id_ocorrencia': self.id_ocorrencia,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'severidade': self.severidade,
            'status': self.status,
            'id_usuario_abriu': self.id_usuario_abriu,
            'id_usuario_solicitante': self.id_usuario_solicitante,
            'id_usuario_relacionado': self.id_usuario_relacionado,
            'id_patrimonio_relacionado': self.id_patrimonio_relacionado,
            'data_abertura': self.data_abertura,
            'data_fechamento': self.data_fechamento,
            'data_alteracao': self.data_alteracao,
            'alterado_por': self.alterado_por
        }
