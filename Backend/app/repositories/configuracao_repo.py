"""
Repository para Configurações do Sistema (registro singleton ID=1)
"""
from typing import Dict, Any, Optional
from app.core.database import get_cursor

TABLE_NAME = "ESTOQUES_TI_CONFIGURACOES"
DEFAULTS = {
    'id_config': 1,
    'nome_empresa': 'Controle de Estoque',
    'modo_escuro': False,
    'alerta_estoque_minimo': 5,
}


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_config': int(row[0]),
        'nome_empresa': row[1] or DEFAULTS['nome_empresa'],
        'modo_escuro': str(row[2] or 'N').upper() == 'S',
        'alerta_estoque_minimo': int(row[3] if row[3] is not None else 5),
    }


class ConfiguracaoRepository:
    @staticmethod
    def garantir_registro() -> Dict[str, Any]:
        """Garante que a linha ID=1 exista e a retorna."""
        with get_cursor() as cursor:
            cursor.execute(
                f"""
                SELECT ID_CONFIG, NOME_EMPRESA, MODO_ESCURO, ALERTA_ESTOQUE_MINIMO
                FROM {TABLE_NAME}
                WHERE ID_CONFIG = 1
                """
            )
            row = cursor.fetchone()
            if row:
                return _row_to_dict(row)

            cursor.execute(
                f"""
                INSERT INTO {TABLE_NAME}
                    (ID_CONFIG, NOME_EMPRESA, MODO_ESCURO, ALERTA_ESTOQUE_MINIMO)
                VALUES
                    (1, :nome, 'N', 5)
                """,
                {'nome': DEFAULTS['nome_empresa']},
            )
            return dict(DEFAULTS)

    @staticmethod
    def obter() -> Dict[str, Any]:
        return ConfiguracaoRepository.garantir_registro()

    @staticmethod
    def atualizar(dados: Dict[str, Any]) -> Dict[str, Any]:
        atual = ConfiguracaoRepository.garantir_registro()

        nome = dados.get('nome_empresa', atual['nome_empresa'])
        modo = dados.get('modo_escuro', atual['modo_escuro'])
        alerta = dados.get('alerta_estoque_minimo', atual['alerta_estoque_minimo'])
        modo_flag = 'S' if bool(modo) else 'N'

        with get_cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE {TABLE_NAME}
                SET NOME_EMPRESA = :nome,
                    MODO_ESCURO = :modo,
                    ALERTA_ESTOQUE_MINIMO = :alerta
                WHERE ID_CONFIG = 1
                """,
                {
                    'nome': nome,
                    'modo': modo_flag,
                    'alerta': int(alerta),
                },
            )

        return ConfiguracaoRepository.obter()
