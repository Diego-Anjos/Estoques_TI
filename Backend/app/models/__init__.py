"""
Models - Classes de domínio que representam as tabelas do banco Oracle
"""
from app.models.usuarios import Usuario
from app.models.locais import Local
from app.models.tipos_item import TipoItem
from app.models.itens import Item
from app.models.estoque_saldo import EstoqueSaldo
from app.models.estoque_movimentacoes import EstoqueMovimentacao
from app.models.patrimonios import Patrimonio
from app.models.patrimonio_atributos import PatrimonioAtributo
from app.models.softwares import Software
from app.models.software_licencas_pool import SoftwareLicencaPool
from app.models.software_atribuicoes import SoftwareAtribuicao
from app.models.ocorrencias import Ocorrencia
from app.models.configuracao import ConfiguracaoSistema

__all__ = [
    'Usuario',
    'Local',
    'TipoItem',
    'Item',
    'EstoqueSaldo',
    'EstoqueMovimentacao',
    'Patrimonio',
    'PatrimonioAtributo',
    'Software',
    'SoftwareLicencaPool',
    'SoftwareAtribuicao',
    'Ocorrencia',
    'ConfiguracaoSistema',
]
