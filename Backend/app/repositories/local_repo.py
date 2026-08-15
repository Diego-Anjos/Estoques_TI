"""
Repository para operações de banco de dados relacionadas a Locais
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor

# Nome da tabela no PostgreSQL
TABLE_NAME = "ESTOQUES_TI_LOCAIS"

_SELECT_COLS = """
    ID_LOCAL, NOME, SETOR, DESCRICAO, STATUS,
    DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
"""


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_local': row[0],
        'nome': row[1],
        'setor': row[2],
        'descricao': row[3],
        'status': row[4] or 'Ativo',
        'data_criacao': row[5],
        'criado_por': row[6],
        'data_alteracao': row[7],
        'alterado_por': row[8],
    }


class LocalRepository:
    """Repository para gerenciar locais no PostgreSQL"""

    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo local"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, SETOR, DESCRICAO, STATUS, CRIADO_POR)
            VALUES (:nome, :setor, :descricao, :status, :criado_por)
            RETURNING ID_LOCAL
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {
                'nome': dados['nome'],
                'setor': dados.get('setor'),
                'descricao': dados.get('descricao'),
                'status': dados.get('status') or 'Ativo',
                'criado_por': usuario_id,
            })
            return cursor.fetchone()[0]

    @staticmethod
    def buscar_por_id(local_id: int) -> Optional[Dict[str, Any]]:
        """Busca local por ID"""
        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME}
            WHERE ID_LOCAL = :id
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {'id': local_id})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def buscar_por_nome(nome: str) -> Optional[Dict[str, Any]]:
        """Busca local por nome"""
        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME}
            WHERE UPPER(NOME) = UPPER(:nome)
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {'nome': nome})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def listar_todos(
        status_filtro: str = "ativos",
        apenas_ativos: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lista locais.
        Por padrão retorna apenas STATUS = 'Ativo' (tabela principal e dropdowns).
        status_filtro: ativos | inativos | todos
        """
        # Compatibilidade com chamadas antigas (apenas_ativos)
        if apenas_ativos is True:
            status_filtro = "ativos"
        elif apenas_ativos is False:
            status_filtro = "todos"

        if status_filtro == "ativos":
            where_sql = "WHERE STATUS = 'Ativo'"
        elif status_filtro == "inativos":
            where_sql = "WHERE STATUS = 'Inativo'"
        else:
            where_sql = ""

        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME}
            {where_sql}
            ORDER BY NOME
        """

        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [_row_to_dict(row) for row in rows]

    @staticmethod
    def inativar(local_id: int, alterado_por: Optional[int] = None) -> bool:
        """Soft-delete: marca o local como Inativo (preserva FKs)."""
        return LocalRepository.atualizar(
            local_id,
            {'status': 'Inativo'},
            alterado_por=alterado_por,
        )

    @staticmethod
    def atualizar(local_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um local"""
        campos = []
        params = {'id': local_id, 'alterado_por': alterado_por}

        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']

        if 'setor' in dados:
            campos.append("SETOR = :setor")
            params['setor'] = dados['setor']

        if 'descricao' in dados:
            campos.append("DESCRICAO = :descricao")
            params['descricao'] = dados['descricao']

        if 'status' in dados:
            campos.append("STATUS = :status")
            params['status'] = dados['status']

        if not campos:
            return False

        campos.append("DATA_ALTERACAO = NOW()")
        campos.append("ALTERADO_POR = :alterado_por")

        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_LOCAL = :id"

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0

    @staticmethod
    def deletar(local_id: int) -> bool:
        """Deleta um local"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_LOCAL = :id"

        with get_cursor() as cursor:
            cursor.execute(sql, {'id': local_id})
            return cursor.rowcount > 0
