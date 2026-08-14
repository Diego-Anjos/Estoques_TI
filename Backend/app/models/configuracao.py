"""
Model para tabela CONFIGURACOES (singleton do sistema)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfiguracaoSistema:
    """Preferências globais do sistema (sempre ID = 1)"""
    id_config: int = 1
    nome_empresa: str = "Controle de Estoque"
    modo_escuro: bool = False
    alerta_estoque_minimo: int = 5

    def to_dict(self) -> dict:
        return {
            'id_config': self.id_config,
            'nome_empresa': self.nome_empresa,
            'modo_escuro': self.modo_escuro,
            'alerta_estoque_minimo': self.alerta_estoque_minimo,
        }
